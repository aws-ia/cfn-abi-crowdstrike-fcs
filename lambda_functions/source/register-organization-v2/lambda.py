"""Function to register AWS Organization with CrowdStrike"""
# pylint: disable=line-too-long,E0401,W1201,C0209
import json
import logging
import os
import sys
import base64
import subprocess
import boto3
import requests
from botocore.exceptions import ClientError

# pip install falconpy package to /tmp/ and add to path
subprocess.call('pip install crowdstrike-falconpy -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')
from falconpy import CSPMRegistration, CloudAWSRegistration

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# CONSTANTS
SUCCESS = "SUCCESS"
FAILED = "FAILED"

VERSION = "1.3.0"
NAME = "crowdstrike-cloud-abi"
USERAGENT = ("%s/%s" % (NAME, VERSION))

SECRET_STORE_NAME = os.environ['secret_name']
SECRET_STORE_REGION = os.environ['secret_region']
EXISTING_CLOUDTRAIL = eval(os.environ['existing_cloudtrail'])
AWS_REGION = os.environ['AWS_REGION']
CS_CLOUD = os.environ['cs_cloud']
AWS_ACCOUNT_TYPE = os.environ['aws_account_type']
FALCON_ACCOUNT_TYPE = os.environ['falcon_account_type']
IDENTITY_PROTECTION = eval(os.environ['identity_protection'])

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

def get_management_id():
    """Function to get Organization Id"""
    org = boto3.client('organizations')
    try:
        org_id = org.list_roots()['Roots'][0]['Arn'].rsplit('/')[1]
        return org_id
    except ClientError:
        logger.error('This stack runs only on the management of the AWS Organization')
        return False

def get_active_regions(exclude_regions):
    """Function to get active Regions"""
    session = boto3.session.Session()
    client = session.client(
        service_name='ec2',
        region_name=AWS_REGION
    )
    supported_regions = [
        "af-south-1",
        "ap-east-1",
        "ap-northeast-1",
        "ap-northeast-2",
        "ap-south-1",
        "ap-southeast-1",
        "ap-southeast-2",
        "ca-central-1",
        "eu-central-1",
        "eu-north-1",
        "eu-south-1",
        "eu-west-1",
        "eu-west-2",
        "eu-west-3",
        "me-south-1",
        "sa-east-1",
        "us-east-1",
        "us-east-2",
        "us-west-1",
        "us-west-2"
    ]
    active_regions = []
    my_regions = []
    comm_gov_eb_regions = []
    ssm_regions = []
    try:
        describe_regions_response = client.describe_regions(AllRegions=False)
        regions = describe_regions_response['Regions']
        for region in regions:
            active_regions += [region['RegionName']]
        for region in active_regions:
            if region not in exclude_regions:
                my_regions += [region]
        for region in active_regions:
            if region in my_regions and region != AWS_REGION:
                comm_gov_eb_regions += [region]
        for region in my_regions:
            if region in supported_regions:
                ssm_regions += [region]
        return my_regions, comm_gov_eb_regions, ssm_regions
    except ClientError as e:
        return e

def process_account(falcon_cspm, aws_account_id, org_id):
    """Get and create or update account registration status"""
    logger.info('Checking for existing registration...')
    response = falcon_cspm.get_aws_account(organization_ids=org_id,
                                        user_agent=USERAGENT)
    logger.info('Get Account Registration Response: %s' % response)
    if response['status_code'] == 207:
        account_response = register_account(falcon_cspm, aws_account_id, org_id)
    elif response['status_code'] == 200:
        account_response = update_account(falcon_cspm, aws_account_id, org_id)
    else:
        account_response = response
    return account_response

def process_features(falcon_cloud, aws_account_id, org_id):
    """Function to process feature registration"""
    logger.info('Checking for existing features...')
    response = falcon_cloud.get_accounts(ids=aws_account_id,
                                        user_agent=USERAGENT)
    logger.info('Get Features Registration Response: %s' % response)
    if response['status_code'] == 207:
        register_features(falcon_cloud, aws_account_id, org_id)
    elif response['status_code'] == 200:
        update_features(falcon_cloud, aws_account_id, org_id)
    else:
        error = response['body']['errors'][0]['message']
        logger.error('Feature Registration Failed with reason....%s' % error)

def register_account(falcon_cspm, aws_account_id, org_id):
    """Function to register account with CSPM"""
    if EXISTING_CLOUDTRAIL:
        response = falcon_cspm.create_aws_account(account_id=aws_account_id,
                                                organization_id=org_id,
                                                behavior_assessment_enabled=True,
                                                sensor_management_enabled=True,
                                                dspm_enabled=True,
                                                dspm_role='CrowdStrikeDSPMIntegrationRole',
                                                use_existing_cloudtrail=EXISTING_CLOUDTRAIL,
                                                user_agent=USERAGENT,
                                                is_master=True,
                                                account_type=AWS_ACCOUNT_TYPE
                                                )
    else:
        response = falcon_cspm.create_aws_account(account_id=aws_account_id,
                                                organization_id=org_id,
                                                behavior_assessment_enabled=True,
                                                sensor_management_enabled=True,
                                                dspm_enabled=True,
                                                dspm_role='CrowdStrikeDSPMIntegrationRole',
                                                use_existing_cloudtrail=EXISTING_CLOUDTRAIL,
                                                cloudtrail_region=AWS_REGION,
                                                user_agent=USERAGENT,
                                                is_master=True,
                                                account_type=AWS_ACCOUNT_TYPE
                                                )
    logger.info('Account Registration Response: %s' % response)
    return response

def register_features(falcon_cloud, aws_account_id, org_id):
    """Function to register account with Cloud features"""
    cloud_response = falcon_cloud.create_account(account_id=aws_account_id,
                                        organization_id=org_id,
                                        user_agent=USERAGENT,
                                        is_master=True,
                                        account_type=AWS_ACCOUNT_TYPE,
                                        products=[
                                                    {
                                                        "features":["default"],
                                                        "product": "idp"
                                                    }
                                                ]
                                        )
    logger.info('Feature Registration Response: %s' % cloud_response)

def update_account(falcon_cspm, aws_account_id, org_id):
    """Function to update CSPM Registration"""
    if EXISTING_CLOUDTRAIL:
        payload = {
            "resources": [
                {
                    'account_id':aws_account_id,
                    'organization_id':org_id,
                    'behavior_assessment_enabled':True,
                    'sensor_management_enabled':True,
                    'dspm_enabled':True,
                    'dspm_role':'CrowdStrikeDSPMIntegrationRole',
                    'use_existing_cloudtrail':EXISTING_CLOUDTRAIL,
                    'user_agent':USERAGENT,
                    'is_master':True,
                    'account_type':AWS_ACCOUNT_TYPE
                }
            ]
        }
    else:
        payload = {
            "resources": [
                {
                    'account_id':aws_account_id,
                    'organization_id':org_id,
                    'behavior_assessment_enabled':True,
                    'sensor_management_enabled':True,
                    'dspm_enabled':True,
                    'dspm_role':'CrowdStrikeDSPMIntegrationRole',
                    'use_existing_cloudtrail':EXISTING_CLOUDTRAIL,
                    'cloudtrail_region':AWS_REGION,
                    'user_agent':USERAGENT,
                    'is_master':True,
                    'account_type':AWS_ACCOUNT_TYPE
                }
            ]
        }
    response = falcon_cspm.update_aws_account(body=payload)
    logger.info('Account Update Response: %s' % response)
    return response

def update_features(falcon_cloud, aws_account_id, org_id):
    """Function to update Cloud features"""
    cloud_response = falcon_cloud.update_account(account_id=aws_account_id,
                                        organization_id=org_id,
                                        user_agent=USERAGENT,
                                        is_master=True,
                                        account_type=AWS_ACCOUNT_TYPE,
                                        products=[
                                                    {
                                                        "features":["default"],
                                                        "product": "idp"
                                                    }
                                                ]
                                        )
    logger.info('Feature Update Response: %s' % cloud_response)

def format_response(response, regions, ssm_regions, comm_gov_eb_regions):
    """Function to format response for CloudFormation"""
    cs_account = response['body']['resources'][0]['intermediate_role_arn'].rsplit('::')[1]
    response_d = {
        "cs_account_id": cs_account.rsplit(':')[0],
        "iam_role_name": response['body']['resources'][0]['iam_role_arn'].rsplit('/')[1],
        "intermediate_role_arn": response['body']['resources'][0]['intermediate_role_arn'],
        "cs_role_name": response['body']['resources'][0]['intermediate_role_arn'].rsplit('/')[1],
        "external_id": response['body']['resources'][0]['external_id'],
        "dspm_role_arn": response['body']['resources'][0]['dspm_role_arn']
    }
    if not EXISTING_CLOUDTRAIL:
        response_d['cs_bucket_name'] = response['body']['resources'][0]['aws_cloudtrail_bucket_name']
    if FALCON_ACCOUNT_TYPE == "commercial":
        response_d['eventbus_name'] = response['body']['resources'][0]['eventbus_name']
        response_d['my_regions'] = regions
        response_d['ssm_regions'] = ssm_regions
    elif FALCON_ACCOUNT_TYPE == "govcloud" and AWS_ACCOUNT_TYPE == "govcloud" :
        eventbus_name = response['body']['resources'][0]['eventbus_name'].rsplit(',')[0]
        response_d['eventbus_name'] = eventbus_name
        response_d['my_regions'] = regions
        response_d['ssm_regions'] = ssm_regions
    elif FALCON_ACCOUNT_TYPE == "govcloud" and AWS_ACCOUNT_TYPE == "commercial" :
        response_d['comm_gov_eb_regions'] = comm_gov_eb_regions
        response_d['my_regions'] = regions
        response_d['ssm_regions'] = ssm_regions
    return response_d

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
    """Function handler"""
    logger.info('Got event %s' % event)
    logger.info('Context %s' % context)
    exclude_regions = event['ResourceProperties']['ExcludeRegions']
    aws_account_id = context.invoked_function_arn.split(":")[4]
    regions, comm_gov_eb_regions, ssm_regions = get_active_regions(exclude_regions)
    org_id = get_management_id()
    try:
        secret_str = get_secret()
        if secret_str:
            secrets_dict = json.loads(secret_str)
            falcon_client_id = secrets_dict['FalconClientId']
            falcon_secret = secrets_dict['FalconSecret']
            falcon_cspm = CSPMRegistration(client_id=falcon_client_id,
                                          client_secret=falcon_secret,
                                          base_url=CS_CLOUD,
                                          user_agent=USERAGENT
                                          )
            if event['RequestType'] in ['Delete']:
                if IDENTITY_PROTECTION:
                    falcon_cloud = CloudAWSRegistration(client_id=falcon_client_id,
                                                       client_secret=falcon_secret,
                                                       user_agent=USERAGENT
                                                       )
                    falcon_cloud.delete_account(organization_ids=org_id,
                                               user_agent=USERAGENT
                                               )
                response = falcon_cspm.delete_aws_account(organization_ids=org_id,
                                                         user_agent=USERAGENT
                                                         )
                cfnresponse_send(event, 'SUCCESS', response['body'], "CustomResourcePhysicalID")
            else:
                response = process_account(falcon_cspm, aws_account_id, org_id)
                if response['status_code'] == 201 or response['status_code'] == 200:
                    response_d = format_response(response, regions, ssm_regions, comm_gov_eb_regions)
                    if IDENTITY_PROTECTION:
                        falcon_cloud = CloudAWSRegistration(client_id=falcon_client_id,
                                                           client_secret=falcon_secret,
                                                           user_agent=USERAGENT
                                                           )
                        process_features(falcon_cloud, aws_account_id, org_id)
                    cfnresponse_send(event, SUCCESS, response_d, "CustomResourcePhysicalID")
                else:
                    error = response['body']['errors'][0]['message']
                    logger.info('Account Registration Failed with reason....%s' % error)
                    response_d = {
                        "reason": response['body']['errors'][0]['message']
                    }
                    cfnresponse_send(event, FAILED, response_d, "CustomResourcePhysicalID")
    except Exception as err:
        logger.info('Registration Failed %s' % err)
        error = str(err)
        response_d = {"reason": error}
        cfnresponse_send(event, FAILED, response_d, "CustomResourcePhysicalID")
