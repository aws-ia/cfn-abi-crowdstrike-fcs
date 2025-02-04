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
GOV_CLOUD = os.environ['gov_cloud']
VERSION = "1.1.1"
NAME = "crowdstrike-cloud-aws-ecr"
USERAGENT = ("%s/%s" % (NAME, VERSION))
ROLE_POLICY_ARN = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
ROLE_NAME = "CrowdStrikeECRConnectionRole"

def get_secret():
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
        raise e
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    return secret

def create_role(external_id, unique_suffix):
    """Function to create the IAM Role for ECR Registry Connection to CrowdStrike"""
    # commercial_principal = "arn:aws:iam::292230061137:role/CrowdStrikeCustomerRegistryAssessmentRole"
    # govcloud_principal = ""
    connection_role = f"{ROLE_NAME}-{unique_suffix}"
    trust_policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": CROWDSTRIKE_PRINCIPAL
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
        PolicyArn='arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly'
    )

    return role['Role']['Arn']

def get_regions():
    """Function getting active AWS Regions."""
    client = boto3.client('ec2')
    regions = client.describe_regions()['Regions']

    return regions

def register_ecr(regions, role_arn, external_id, falcon_client_id, falcon_secret, account):
    """Function to register ECR in each region with CrowdStrike"""
    falcon = FalconContainer(client_id=falcon_client_id,
                             client_secret=falcon_secret
                            )
    for i in regions:
        region_name = i["RegionName"]
        print(f'Processing region: {region_name}')
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
                             client_secret=falcon_secret
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
                             client_secret=falcon_secret
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
    try:
        response = requests.put(response_url,
                                data=json_response_body,
                                headers=headers,
                                timeout=5)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

def generate_ids():
    ssm = boto3.client('ssm')
    external_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    unique_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    try:
        ssm.put_parameter(
            Name='crowdstrike-ecr-lambda-role-id',
            Description='Unique ID for creating CrowdStrike ECR Registry Connection Role',
            Value=unique_suffix,
            Type='String',
            Overwrite=False,
            Tier='Standard'
        )
        ssm.put_parameter(
            Name='crowdstrike-ecr-lambda-external-id',
            Description='External ID for creating trust policy for CrowdStrike ECR Registry Connection Role',
            Value=external_id,
            Type='String',
            Overwrite=False,
            Tier='Standard'
        )
    except Exception as e:
        print("send(..) failed creating SSM Parameters(..): " + str(e))
    
    return external_id, unique_suffix

def delete_role():
    ssm = boto3.client('ssm')
    iam = boto3.client('iam')
    print("Deleting IAM Role...")
    try:
        response = ssm.get_parameter(
            Name='crowdstrike-ecr-lambda-role-id'
        )
        unique_suffix = response['Parameter']['Value']
        connection_role = f"{ROLE_NAME}-{unique_suffix}"
        iam.detach_role_policy(
            RoleName=connection_role,
            PolicyArn=ROLE_POLICY_ARN
        )
        response = iam.delete_role(
            RoleName=connection_role
        )
        print(f'Response: {response}')
        ssm.delete_parameter(
            Name='crowdstrike-ecr-lambda-role-id'
        )
    except Exception as e:
        print("send(..) failed deleting the connection role(..): " + str(e))

def lambda_handler(event, context):
    """Main Function"""
    logger.info('Got event %s' % event)
    logger.info('Context %s' % context)
    account = boto3.client('sts').get_caller_identity().get('Account')
    response = {}
    try:
        secret_str = get_secret()
        if secret_str:
            secrets_dict = json.loads(secret_str)
            falcon_client_id = secrets_dict['FalconClientId']
            falcon_secret = secrets_dict['FalconSecret']
            if event['RequestType'] in ['Create']:
                external_id, unique_suffix = generate_ids()
                role_arn = create_role(external_id, unique_suffix)
                print(f'Created role:\n{role_arn}\n')
                regions = get_regions()
                register_ecr(regions, role_arn, external_id, falcon_client_id, falcon_secret, account)
                print('ECR Connection registration complete!')
                cfnresponse_send(event, SUCCESS, response, "CustomResourcePhysicalID")
            # elif event['RequestType'] in ['Delete']:
            #     local_entities = get_entities(falcon_client_id, falcon_secret, account)
            #     delete_entities(falcon_client_id, falcon_secret, local_entities)
            #     delete_role()
            #     print("Complete!")
            #     cfnresponse_send(event, SUCCESS, response, "CustomResourcePhysicalID")
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