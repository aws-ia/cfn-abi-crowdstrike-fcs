# type: ignore
"""Custom Resource to get AWS Organization ID.

Version: 1.0

Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0
"""
import logging
import os

import boto3
import cfnresponse

LOGGER = logging.getLogger(__name__)
log_level: str = os.environ.get("LOG_LEVEL", "ERROR")
LOGGER.setLevel(log_level)
EVENTBUS_ACCOUNT = os.environ.get('EVENTBUS_ACCOUNT')
EKS_PROTECTION = os.environ.get('EKS_PROTECTION')


def get_org_id():
    """Get AWS Organization ID.

    Returns:
        Response data for custom resource
    """
    management_account_session = boto3.Session()
    org_client = management_account_session.client("organizations")
    response = org_client.describe_organization()["Organization"]
    organization_id = response["Id"]
    LOGGER.debug({"API_Call": "organizations:DescribeOrganization", "API_Response": response})
    return organization_id

def get_parents():
    """Get AWS Organization ID.

    Returns:
        Response data for custom resource
    """
    management_account_session = boto3.Session()
    org_client = management_account_session.client("organizations")
    response = org_client.list_parents(ChildId=EVENTBUS_ACCOUNT).get('Parents')
    eventbus_account_ou = response[0].get('Id')
    LOGGER.debug({"API_Call": "organizations:ListParents", "API_Response": response})
    return eventbus_account_ou

def lambda_handler(event, context):
    """Lambda Handler.

    Args:
        event: event data
        context: runtime information
    """
    try:
        data_dict = {}
        organization_id = get_org_id()
        data_dict['organization_id'] = organization_id
        if EKS_PROTECTION == "true":
            eventbus_account_ou = get_parents()
            data_dict['eventbus_account_ou'] = eventbus_account_ou
        cfnresponse.send(event, context, cfnresponse.SUCCESS, data_dict, data_dict["organization_id"])
    except Exception:
        LOGGER.exception("Unexpected!")
        reason = f"See the details in CloudWatch Log Stream: '{context.log_group_name}'"
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, data_dict reason=reason)
