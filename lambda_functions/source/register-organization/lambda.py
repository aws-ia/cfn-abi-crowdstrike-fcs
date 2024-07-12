import json
import logging
import os
import sys
import subprocess
import boto3
import requests
import base64
from botocore.exceptions import ClientError

# pip install falconpy package to /tmp/ and add to path
subprocess.call('pip install crowdstrike-falconpy -t /tmp/ --no-cache-dir'.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
sys.path.insert(1, '/tmp/')
from falconpy import CSPMRegistration

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# CONSTANTS
SUCCESS = "SUCCESS"
FAILED = "FAILED"

VERSION = "1.0.0"
name = "crowdstrike-cloud-abi"
useragent = ("%s/%s" % (name, VERSION))

SECRET_STORE_NAME = os.environ['secret_name']
SECRET_STORE_REGION = os.environ['secret_region']
EXCLUDE_REGIONS = os.environ['exclude_regions']
EXISTING_CLOUDTRAIL = eval(os.environ['existing_cloudtrail'])
AWS_REGION = os.environ['AWS_REGION']
CS_CLOUD = os.environ['cs_cloud']
AWS_ACCOUNT_TYPE = os.environ['aws_account_type']
FALCON_ACCOUNT_TYPE = os.environ['falcon_account_type']

def get_secret():
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
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            raise e
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return secret

def get_management_id():
    ORG = boto3.client('organizations')
    try:
        orgIDstr = ORG.list_roots()['Roots'][0]['Arn'].rsplit('/')[1]
        return orgIDstr
    except Exception as e:
        logger.error('This stack runs only on the management of the AWS Organization')
        return False

def get_active_regions():
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
            if region not in EXCLUDE_REGIONS:
                my_regions += [region]
        for region in active_regions:
            if region in my_regions and region != AWS_REGION:
                comm_gov_eb_regions += [region]
        for region in my_regions:
            if region in supported_regions:
                ssm_regions += [region]
        return my_regions, comm_gov_eb_regions, ssm_regions
    except Exception as e:
        return e
    
def cfnresponse_send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False):
    responseUrl = event['ResponseURL']
    print(responseUrl)
    responseBody = {}
    responseBody['Status'] = responseStatus
    responseBody['Reason'] = 'See the details in CloudWatch Log Stream: '
    responseBody['PhysicalResourceId'] = physicalResourceId
    responseBody['StackId'] = event['StackId']
    responseBody['RequestId'] = event['RequestId']
    responseBody['LogicalResourceId'] = event['LogicalResourceId']
    responseBody['Data'] = responseData
    json_responseBody = json.dumps(responseBody)
    print("Response body:\n" + json_responseBody)
    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }
    try:
        response = requests.put(responseUrl,
                                data=json_responseBody,
                                headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("send(..) failed executing requests.put(..): " + str(e))

def lambda_handler(event, context):
    logger.info('Got event {}'.format(event))
    logger.info('Context {}'.format(context))
    aws_account_id = context.invoked_function_arn.split(":")[4]
    regions, comm_gov_eb_regions, ssm_regions = get_active_regions()
    OrgId = get_management_id()
    try:
        secret_str = get_secret()
        if secret_str:
            secrets_dict = json.loads(secret_str)
            FalconClientId = secrets_dict['FalconClientId']
            FalconSecret = secrets_dict['FalconSecret']
            falcon = CSPMRegistration(client_id=FalconClientId,
                                    client_secret=FalconSecret,
                                    base_url=CS_CLOUD,
                                    user_agent=useragent
                                    )
            if event['RequestType'] in ['Create']:
                logger.info('Event = {}'.format(event))
                if EXISTING_CLOUDTRAIL:
                    response = falcon.create_aws_account(account_id=aws_account_id,
                                                        organization_id=OrgId,
                                                        behavior_assessment_enabled=True,
                                                        sensor_management_enabled=True,
                                                        use_existing_cloudtrail=EXISTING_CLOUDTRAIL,
                                                        user_agent=useragent,
                                                        is_master=True,
                                                        account_type=AWS_ACCOUNT_TYPE
                                                        )                    
                else:
                    response = falcon.create_aws_account(account_id=aws_account_id,
                                                        organization_id=OrgId,
                                                        behavior_assessment_enabled=True,
                                                        sensor_management_enabled=True,
                                                        use_existing_cloudtrail=EXISTING_CLOUDTRAIL,
                                                        cloudtrail_region=AWS_REGION,
                                                        user_agent=useragent,
                                                        is_master=True,
                                                        account_type=AWS_ACCOUNT_TYPE
                                                        )
                logger.info('Response: {}'.format(response))
                if response['status_code'] == 201:
                    cs_account = response['body']['resources'][0]['intermediate_role_arn'].rsplit('::')[1]
                    response_d = {
                        "cs_account_id": cs_account.rsplit(':')[0],
                        "iam_role_name": response['body']['resources'][0]['iam_role_arn'].rsplit('/')[1],
                        "intermediate_role_arn": response['body']['resources'][0]['intermediate_role_arn'],
                        "cs_role_name": response['body']['resources'][0]['intermediate_role_arn'].rsplit('/')[1],
                        "external_id": response['body']['resources'][0]['external_id']
                    }
                    if not EXISTING_CLOUDTRAIL:
                        response_d['cs_bucket_name'] = response['body']['resources'][0]['aws_cloudtrail_bucket_name']
                    if FALCON_ACCOUNT_TYPE == "commercial":
                        response_d['eventbus_name'] = response['body']['resources'][0]['eventbus_name']
                        response_d['my_regions'] = regions
                        response_d['ssm_regions'] = ssm_regions
                    elif FALCON_ACCOUNT_TYPE == "govcloud" and AWS_ACCOUNT_TYPE == "govcloud" :
                        response_d['eventbus_name'] = response['body']['resources'][0]['eventbus_name'].rsplit(',')[0]
                        response_d['my_regions'] = regions
                        response_d['ssm_regions'] = ssm_regions
                    elif FALCON_ACCOUNT_TYPE == "govcloud" and AWS_ACCOUNT_TYPE == "commercial" :
                        response_d['comm_gov_eb_regions'] = comm_gov_eb_regions
                        response_d['my_regions'] = regions
                        response_d['ssm_regions'] = ssm_regions
                    cfnresponse_send(event, context, SUCCESS, response_d, "CustomResourcePhysicalID")
                elif 'already exists' in response['body']['errors'][0]['message']:
                    logger.info(response['body']['errors'][0]['message'])
                    logger.info('Getting existing registration data...')
                    response = falcon.get_aws_account(organization_id=OrgId)
                    logger.info('Existing Registration Response: {}'.format(response))
                    cs_account = response['body']['resources'][0]['intermediate_role_arn'].rsplit('::')[1]
                    response_d = {
                        "cs_account_id": cs_account.rsplit(':')[0],
                        "iam_role_name": response['body']['resources'][0]['iam_role_arn'].rsplit('/')[1],
                        "intermediate_role_arn": response['body']['resources'][0]['intermediate_role_arn'],
                        "cs_role_name": response['body']['resources'][0]['intermediate_role_arn'].rsplit('/')[1],
                        "external_id": response['body']['resources'][0]['external_id']
                    }
                    if not EXISTING_CLOUDTRAIL:
                        response_d['cs_bucket_name'] = response['body']['resources'][0]['aws_cloudtrail_bucket_name']
                    if FALCON_ACCOUNT_TYPE == "commercial":
                        response_d['eventbus_name'] = response['body']['resources'][0]['eventbus_name']
                        response_d['my_regions'] = regions
                        response_d['ssm_regions'] = ssm_regions
                    elif FALCON_ACCOUNT_TYPE == "govcloud" and AWS_ACCOUNT_TYPE == "govcloud" :
                        response_d['eventbus_name'] = response['body']['resources'][0]['eventbus_name'].rsplit(',')[0]
                        response_d['my_regions'] = regions
                        response_d['ssm_regions'] = ssm_regions
                    elif FALCON_ACCOUNT_TYPE == "govcloud" and AWS_ACCOUNT_TYPE == "commercial" :
                        response_d['comm_gov_eb_regions'] = comm_gov_eb_regions
                        response_d['my_regions'] = regions
                        response_d['ssm_regions'] = ssm_regions
                    cfnresponse_send(event, context, SUCCESS, response_d, "CustomResourcePhysicalID")
                else:
                    error = response['body']['errors'][0]['message']
                    logger.info('Account Registration Failed with reason....{}'.format(error))
                    response_d = {
                        "reason": response['body']['errors'][0]['message']
                    }
                    cfnresponse_send(event, context, FAILED, response_d, "CustomResourcePhysicalID")
            elif event['RequestType'] in ['Update']:
                response_d = {}
                logger.info('Event = ' + event['RequestType'])
                cfnresponse_send(event, context, SUCCESS, response_d, "CustomResourcePhysicalID")
            elif event['RequestType'] in ['Delete']:
                logger.info('Event = ' + event['RequestType'])
                response = falcon.delete_aws_account(organization_ids=OrgId,
                                                    user_agent=useragent
                                                    )
                cfnresponse_send(event, context, 'SUCCESS', response['body'], "CustomResourcePhysicalID")
    except Exception as err:  # noqa: E722
        # We can't communicate with the endpoint
        logger.info('Registration Failed {}'.format(err))
        cfnresponse_send(event, context, FAILED, err, "CustomResourcePhysicalID")