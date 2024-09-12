"""Function running CrowdStrike EKS Protection for existing EKS Clusters."""
import json
import os
import logging
from datetime import date
import botocore
import boto3
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# CONSTANTS
SUCCESS = "SUCCESS"
FAILED = "FAILED"

DATE = date.today()
PROJECT = os.environ['project_name']
BUCKET = os.environ['artifact_bucket']
REGION = os.environ['AWS_DEFAULT_REGION']
SWITCH_ROLE = os.environ['lambda_switch_role']

def accounts():
    """Function getting AWS Account list."""
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='organizations',
            region_name=REGION
        )
        response = client.list_accounts()
        response_accounts = response['Accounts']
        next_token = response.get('NextToken', None)

        while next_token:
            response = client.list_accounts(NextToken=next_token)
            response_accounts += response['Accounts']
            next_token = response.get('NextToken', None)

        active_accounts = [a for a in response_accounts if a['Status'] == 'ACTIVE']
        return active_accounts
    except client.exceptions.AccessDeniedException:
        print("Cannot autodiscover adjacent accounts: \
              cannot list accounts within the AWS organization")
        return None

def new_session(account_id, region):
    """Function establishing boto3 session."""
    try:
        sts_connection = boto3.client('sts')
        credentials = sts_connection.assume_role(
            RoleArn=f'arn:aws:iam::{account_id}:role/{SWITCH_ROLE}',
            RoleSessionName=f'crowdstrike-eks-{account_id}'
        )
        return boto3.session.Session(
            aws_access_key_id=credentials['Credentials']['AccessKeyId'],
            aws_secret_access_key=credentials['Credentials']['SecretAccessKey'],
            aws_session_token=credentials['Credentials']['SessionToken'],
            region_name=region
        )
    except sts_connection.exceptions.ClientError as exc:
        # Print the error and continue.
        # Handle what to do with accounts that cannot be accessed
        # due to assuming role errors.
        print("Cannot access adjacent account: ", account_id, exc)
        return None


def regions():
    """Function getting active AWS Regions."""
    session = boto3.session.Session()
    client = session.client(
        service_name='ec2',
        region_name=REGION
    )

    active_regions = client.describe_regions()['Regions']
    return active_regions


def clusters(session, region_name):
    """Function getting EKS Clusters."""
    client = session.client(
        service_name='eks',
        region_name=region_name
    )

    response = client.list_clusters(maxResults=100)
    eks_clusters = response['clusters']
    next_token = response['NextToken'] if 'NextToken' in response else None

    while next_token:
        response = client.list_clusters(maxResults=100, NextToken=next_token)
        eks_clusters += response['clusters']
        next_token = response['NextToken'] if 'NextToken' in response else None

    return eks_clusters

def describe_cluster(session, region_name, cluster_name):
    """Function checking EKS Cluster."""
    client = session.client(
        service_name='eks',
        region_name=region_name
    )

    response = client.describe_cluster(name=cluster_name)
    cluster_arn = response.get('cluster', {}).get('arn')
    auth_mode = response.get('cluster', {}).get('accessConfig', \
                             {}).get('authenticationMode')
    public_endpoint = response.get('cluster', {}).get('resourcesVpcConfig', \
                                   {}).get('endpointPublicAccess')

    return cluster_arn, auth_mode, public_endpoint

def check_fargate(session, region_name, cluster_name):
    """Function checking for Fargate."""
    client = session.client(
        service_name='eks',
        region_name=region_name
    )

    try:
        response = client.list_fargate_profiles(
            clusterName=cluster_name,
            maxResults=10
        )
        if response['fargateProfileNames'] not in []:
            logger.info('No fargate profiles found, setting node_type to nodegroup...')
            node_type = 'nodegroup'
        else:
            node_type = 'fargate'
        return node_type
    except botocore.exceptions.ClientError as error:
        logger.error(error)
        return None

def start_build(cluster_name, cluster_arn, node_type, account_id, region_name):
    """Function running CodeBuild for EKS Protection."""
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='codebuild',
            region_name=REGION
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
        logger.info('Started build %s, buildId %s' % (PROJECT, build_id))
    except botocore.exceptions.ClientError as error:
        logger.error(error)

def cfnresponse_send(event, response_status, response_data, physical_resource_id=None):
    """Function sending response to CloudFormation."""
    response_url = event['ResponseURL']
    print(response_url)
    response_body = {}
    response_body['Status'] = response_status
    response_body['Reason'] = 'See the details in CloudWatch Log Stream: '
    response_body['PhysicalResourceId'] = physical_resource_id
    response_body['StackId'] = event['StackId']
    response_body['RequestId'] = event['RequestId']
    response_body['LogicalResourceId'] = event['LogicalResourceId']
    response_body['Data'] = response_data
    json_response_body = json.dumps(response_body)
    print("Response body:\n" + json_response_body)
    headers = {
        'content-type': '',
        'content-length': str(len(json_response_body))
    }
    try:
        response = requests.put(response_url,
                                data=json_response_body,
                                headers=headers,
                                timeout=5)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

def lambda_handler(event, context):
    """Function handler."""
    logger.info('Got event %s' % event)
    logger.info('Context %s' % context)
    logger.info('Gathering Event Details...')
    response_d = {}
    if event["RequestType"] in ["Create"]:
        try:
            for account in accounts():
                account_id = account['Id']
                for region in regions():
                    region_name = region["RegionName"]
                    session = new_session(account_id, region_name)
                    if session:
                        for cluster_name in clusters(session, region_name):

                            cluster_arn, auth_mode, public_endpoint = describe_cluster(session,
                                                                                       region_name,
                                                                                       cluster_name)
                            if public_endpoint and 'API' in auth_mode:
                                node_type = check_fargate(session, region_name, cluster_name)
                                if node_type:
                                    start_build(cluster_name,
                                                cluster_arn,
                                                node_type,
                                                account_id,
                                                region_name)
                            else:
                                logger.info('Access denied for cluster %s. \
                                            Please verify that API Access and Public \
                                            Endpoint are enabled' % cluster_name)
            response_d['status'] = "success"
            cfnresponse_send(event, SUCCESS, response_d, "CustomResourcePhysicalID")
        except botocore.exceptions.ClientError as error:
            logger.error(error)
            response_d['error'] = error
            cfnresponse_send(event, SUCCESS, response_d, "CustomResourcePhysicalID")
    else:
        response = {"Status": "Complete"}
        cfnresponse_send(event, "SUCCESS", response, "CustomResourcePhysicalID")
