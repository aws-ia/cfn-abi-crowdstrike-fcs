"""Function running CrowdStrike EKS Protection for new EKS Clusters."""
import os
import logging
from datetime import date
import botocore
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

DATE = date.today()
PROJECT = os.environ['project_name']
BUCKET = os.environ['artifact_bucket']
SWITCH_ROLE = os.environ['lambda_switch_role']

def new_session(account_id, region_name):
    """Function establishing boto3 session."""
    try:
        sts_connection = boto3.client('sts')
        credentials = sts_connection.assume_role(
            RoleArn=f'arn:aws:iam::{account_id}:role/{SWITCH_ROLE}',
            RoleSessionName=account_id
        )
        return boto3.session.Session(
            aws_access_key_id=credentials['Credentials']['AccessKeyId'],
            aws_secret_access_key=credentials['Credentials']['SecretAccessKey'],
            aws_session_token=credentials['Credentials']['SessionToken'],
            region_name=region_name
        )
    except sts_connection.exceptions.ClientError as exc:
        # Print the error and continue.
        # Handle what to do with accounts that cannot be accessed
        # due to assuming role errors.
        print("Cannot access adjacent account: ", account_id, exc)
        return None

def start_build(region, cluster_name, cluster_arn, node_type, account_id, region_name):
    """Function running CodeBuild for EKS Protection."""
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='codebuild',
            region_name=region
        )
        build = client.start_build(
            projectName=PROJECT,
            artifactsOverride={
                'type': 'S3',
                'location': f'{BUCKET}',
                'path': 'BuildResults',
                'name': f'{cluster_name}-{DATE}',
                'packaging': 'ZIP'
            },
            environmentVariablesOverride=[
                {
                    'name': 'CLUSTER',
                    'value': f'{cluster_name}',
                    'type': 'PLAINTEXT'
                },
                {
                    'name': 'NODE_TYPE',
                    'value': f'{node_type}',
                    'type': 'PLAINTEXT'
                },
                {
                    'name': 'CLUSTER_ARN',
                    'value': f'{cluster_arn}',
                    'type': 'PLAINTEXT'
                },
                {
                    'name': 'ACCOUNT_ID',
                    'value': f'{account_id}',
                    'type': 'PLAINTEXT'
                },
                {
                    'name': 'REGION',
                    'value': f'{region_name}',
                    'type': 'PLAINTEXT'
                }
            ]
        )
        build_id = build.get('build', {}).get('id')
        logger.info('Started build %s, buildId %s', PROJECT, build_id)
    except botocore.exceptions.ClientError as error:
        logger.error(error)

def lambda_handler(event,context):
    """Function handler."""
    logger.info('Got event %s', event)
    logger.info('Context %s', context)
    logger.info('Gathering Event Details...')
    region_name = event['region']
    account_id = event['detail']['userIdentity']['accountId']
    cluster_name = event['detail']['requestParameters']['name']
    event_name = event['detail']['eventName']
    if 'CreateCluster' in event_name:
        node_type = 'nodegroup'
    elif 'CreateFargateProfile' in event_name:
        node_type = 'fargate'
    else:
        node_type = 'nodegroup'
    logger.info('Checking EKS Cluster for API Access Config..')
    try:
        session = new_session(account_id, region_name)
        client = session.client(
            service_name='eks'
        )
        cluster_details = client.describe_cluster(
            name=cluster_name
        )
        cluster_arn = cluster_details.get('cluster', {}).get('arn')
        auth_mode = cluster_details.get('cluster', {}).get('accessConfig',\
                                        {}).get('authenticationMode')
        public_endpoint = cluster_details.get('cluster', {}).get('resourcesVpcConfig',\
                                              {}).get('endpointPublicAccess')
        if public_endpoint and 'API' in auth_mode:
            start_build(region_name, cluster_name, cluster_arn, node_type, account_id, region_name)
        else:
            logger.info('API Access not enabled on cluster %s', cluster_name)
    except botocore.exceptions.ClientError as error:
        logger.error(error)
