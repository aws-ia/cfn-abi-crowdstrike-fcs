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


def get_org_id():
    """Get AWS Organization ID.

    Returns:
        Response data for custom resource
    """
    management_account_session = boto3.Session()
    org_client = management_account_session.client("organizations")
    response = org_client.describe_organization()["Organization"]
    organization_id = response["Id"]
    parents = org_client.list_parents(ChildId=EVENTBUS_ACCOUNT).get('Parents')
    eventbus_account_ou = parents[0].get('Id')
    LOGGER.debug({"API_Call": "organizations:DescribeOrganization", "API_Response": response})
    return organization_id, eventbus_account_ou

def lambda_handler(event, context):
    """Lambda Handler.

    Args:
        event: event data
        context: runtime information
    """
    try:
        data_dict = {}
        organization_id, eventbus_account_ou = get_org_id()
        data_dict['organization_id'] = organization_id
        data_dict['eventbus_account_ou'] = eventbus_account_ou
        cfnresponse.send(event, context, cfnresponse.SUCCESS, data, data_dict)
    except Exception:
        LOGGER.exception("Unexpected!")
        reason = f"See the details in CloudWatch Log Stream: '{context.log_group_name}'"
        cfnresponse.send(event, context, cfnresponse.FAILED, {}, data_dict, reason=reason)
