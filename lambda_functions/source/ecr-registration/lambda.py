"""Function to register ECR Registries with CrowdStrike"""
# pylint: disable=line-too-long
import json
import logging
import os
import sys
import base64
import subprocess
import random
import string
import time
import boto3
import requests
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# pip install falconpy package to /tmp/ and add to path
subprocess.call('pip install crowdstrike-falconpy -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')
from falconpy import FalconContainer

# CONSTANTS
SUCCESS = "SUCCESS"
FAILED = "FAILED"

SECRET_STORE_NAME = os.environ['secret_name']
SECRET_STORE_REGION = os.environ['secret_region']
PERMISSIONS_BOUNDARY = os.environ['permissions_boundary']
CROWDSTRIKE_PRINCIPAL = os.environ['crowdstrike_principal']
GOV_CLOUD_PRINCIPAL = os.environ['gov_cloud_principal']
GOV_CLOUD = eval(os.environ['gov_cloud'])
COMM_TO_GOV_CLOUD = eval(os.environ['comm_to_gov_cloud'])
STACK_ID = os.environ['stack_id']
VERSION = "1.5.0"
NAME = "crowdstrike-cloud-aws-ecr"
USERAGENT = ("%s/%s" % (NAME, VERSION))
ROLE_POLICY_ARN = os.environ['role_policy_arn']
ROLE_NAME = "CrowdStrikeECRConnectionRole"
DISCONNECT_UPON_DELETE = eval(os.environ['disconnect_upon_delete'])
CS_CLOUD = os.environ['cs_cloud']
REGIONS = os.environ['regions']

def get_secret(event):
    """Function to get secret"""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=SECRET_STORE_REGION
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=SECRET_STORE_NAME
        )
    except ClientError as e:
        error = str(e)
        response = {
            "error": error
        }
        cfnresponse_send(event, FAILED, response, "CustomResourcePhysicalID")
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return secret

def create_role(external_id, STACK_ID):
    """Function to create the IAM Role for ECR Registry Connection to CrowdStrike"""
    connection_role = f"{ROLE_NAME}-{STACK_ID}"
    if GOV_CLOUD:
        principal=GOV_CLOUD_PRINCIPAL
    elif COMM_TO_GOV_CLOUD:
        principal=GOV_CLOUD_PRINCIPAL
    else:
        principal=CROWDSTRIKE_PRINCIPAL
    trust_policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": principal
                },
                "Action": "sts:AssumeRole",
                "Condition": {
                    "StringEquals": {
                        "sts:ExternalId": external_id
                    }
                }
            }
        ]
    })
    client = boto3.client('iam')
    if PERMISSIONS_BOUNDARY:
        role = client.create_role(
            RoleName=connection_role,
            AssumeRolePolicyDocument=trust_policy,
            Description='ReadOnly role to facilitate ECR Registry connections to CrowdStrike for Image Assessment',
            PermissionsBoundary=PERMISSIONS_BOUNDARY
        )
    else:
        role = client.create_role(
            RoleName=connection_role,
            AssumeRolePolicyDocument=trust_policy,
            Description='ReadOnly role to facilitate ECR Registry connections to CrowdStrike for Image Assessment'
        )
    client.attach_role_policy(
        RoleName=connection_role,
        PolicyArn=ROLE_POLICY_ARN
    )
    return role['Role']['Arn']

def get_regions():
    """Function getting active AWS Regions."""
    regions = []
    if REGIONS:
        regions = REGIONS.split(',')
    else:
        client = boto3.client('ec2')
        response = client.describe_regions()['Regions']
        for i in response['Regions']:
            regions.append(i['RegionName'])
    return regions

def register_ecr(regions, role_arn, external_id, falcon_client_id, falcon_secret, account):
    """Function to register ECR in each region with CrowdStrike"""
    falcon = FalconContainer(client_id=falcon_client_id,
                             client_secret=falcon_secret,
                             base_url=CS_CLOUD
                            )
    for i in regions:
        region_name = i.strip()
        print(f'Processing region: {region_name}')
        if GOV_CLOUD:
            payload = {
                "all_repositories_monitored": True,
                "url": f"https://{account}.dkr.ecr.{region_name}.amazonaws.com",
                "credential": {
                    "details": {
                        "aws_iam_role": role_arn,
                        "aws_external_id": external_id,
                        "aws_gov_using_commercial_connection": False
                    },
                    "type": "ecr"
                },
                "type": "ecr"
            }
        elif COMM_TO_GOV_CLOUD:
            payload = {
                "all_repositories_monitored": True,
                "url": f"https://{account}.dkr.ecr.{region_name}.amazonaws.com",
                "credential": {
                    "details": {
                        "aws_iam_role": role_arn,
                        "aws_external_id": external_id,
                        "aws_gov_using_commercial_connection": True
                    },
                    "type": "ecr"
                },
                "type": "ecr"
            }
        else:
            payload = {
                "credential": {
                    "details": {
                        "aws_iam_role": role_arn,
                        "aws_external_id": external_id
                    }
                },
                "type": "ecr",
                "url": f"https://{account}.dkr.ecr.{region_name}.amazonaws.com"
            }
        print(f'Payload: {payload}')
        response = falcon.create_registry_entities(
                                                  body=payload
                                                  )
        print(f'Response: {response}')

def get_entities(falcon_client_id, falcon_secret, account):
    """Function to get ECR Registry Connections for this AWS account"""
    local_entities = []
    falcon = FalconContainer(client_id=falcon_client_id,
                             client_secret=falcon_secret,
                             base_url=CS_CLOUD
                            )
    read_response = falcon.read_registry_entities()
    print(read_response)
    uuids = read_response['body']['resources']
    for i in uuids:
        details = falcon.read_registry_entities_by_uuid(ids=i)
        url = details['body']['resources'][0]['url']
        if account in url:
            local_entities += [i]
    return local_entities

def delete_entities(falcon_client_id, falcon_secret, local_entities):
    """Function to delete ECR Registry Connections for this AWS account"""
    print("Deleting registry connections...")
    falcon = FalconContainer(client_id=falcon_client_id,
                             client_secret=falcon_secret,
                             base_url=CS_CLOUD
                            )
    response = falcon.delete_registry_entities(
                                   ids=local_entities
                                   )
    print(f'Response: {response}')

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
    response = requests.put(response_url,
                            data=json_response_body,
                            headers=headers,
                            timeout=5)
    print("Status code: " + response.reason)

def generate_ids():
    ssm = boto3.client('ssm')
    external_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    ssm.put_parameter(
        Name=f'crowdstrike-ecr-lambda-external-id-{STACK_ID}',
        Description='External ID for creating trust policy for CrowdStrike ECR Registry Connection Role',
        Value=external_id,
        Type='String',
        Overwrite=False,
        Tier='Standard'
    )
    return external_id

def delete_role():
    ssm = boto3.client('ssm')
    iam = boto3.client('iam')
    print("Deleting IAM Role...")
    connection_role = f"{ROLE_NAME}-{STACK_ID}"
    iam.detach_role_policy(
        RoleName=connection_role,
        PolicyArn=ROLE_POLICY_ARN
    )
    response = iam.delete_role(
        RoleName=connection_role
    )
    print(f'Response: {response}')
    ssm.delete_parameter(
        Name=f'crowdstrike-ecr-lambda-external-id-{STACK_ID}'
    )

def lambda_handler(event, context):
    """Main Function"""
    logger.info('Got event %s' % event)
    logger.info('Context %s' % context)
    account = boto3.client('sts').get_caller_identity().get('Account')
    response = {}
    try:
        secret_str = get_secret(event)
        if secret_str:
            secrets_dict = json.loads(secret_str)
            falcon_client_id = secrets_dict['FalconClientId']
            falcon_secret = secrets_dict['FalconSecret']
            if event['RequestType'] in ['Create']:
                external_id = generate_ids()
                role_arn = create_role(external_id, STACK_ID)
                print(f'Created role:\n{role_arn}\n')
                regions = get_regions()
                time.sleep(60)
                register_ecr(regions, role_arn, external_id, falcon_client_id, falcon_secret, account)
                print('ECR Connection registration complete!')
                cfnresponse_send(event, SUCCESS, response, "CustomResourcePhysicalID")
            elif event['RequestType'] in ['Delete']:
                if DISCONNECT_UPON_DELETE:
                    local_entities = get_entities(falcon_client_id, falcon_secret, account)
                    delete_entities(falcon_client_id, falcon_secret, local_entities)
                    delete_role(event)
                    print("Complete!")
                cfnresponse_send(event, SUCCESS, response, "CustomResourcePhysicalID")
            else:
                print("complete")
                cfnresponse_send(event, SUCCESS, response, "CustomResourcePhysicalID")
        else:
            print("complete")
            cfnresponse_send(event, SUCCESS, response, "CustomResourcePhysicalID")
    except Exception as err:
        logger.info('Registration Failed %s' % err)
        error = str(err)
        response = {
            "error": error
        }
        cfnresponse_send(event, FAILED, response, "CustomResourcePhysicalID")