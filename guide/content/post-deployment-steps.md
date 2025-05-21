---
weight: 11
title: Postdeployment options
description: Postdeployment options.
---

## Verifying the solution functionality

### Verify account activation in CrowdStrike Falcon console
1. Sign in to the CrowdStrike Falcon console.
2. Navigate to [Cloud-Security > Registration](https://falcon.crowdstrike.com/cloud-security/registration).
3. Verify that each AWS account ID is active in the **Configuration** (IOM), **Behavior** (IOA) and **1-click sensor deployment** columns.
4. After waiting several minutes, choose **Refresh** to retrieve the latest account status.

### Verify SSM Distributor Package deployments in CrowdStrike Falcon console
1. Sign in to the CrowdStrike Falcon console.
2. Navigate to [Host setup and management > Host management](https://falcon.crowdstrike.com/hosts/hosts?navigationFrom=siteNav).
3. Verify that your AWS Instances begin to appear in the host management list with a Host status of "Online".
4. After waiting several minutes, choose **Refresh** to retrieve the latest host status.

## Update the IAM Role with Latest IOM Permissions

Update the IAM Role in the master account.
1. Download the latest main template [here](https://raw.githubusercontent.com/aws-ia/cfn-abi-crowdstrike-fcs/main/templates/crowdstrike_init_stack.yaml).
3. Sign in to the AWS Account in which you deployed the main stack for this solution.
3. Navigate to `CloudFormation` > `Stacks`
4. Select the main stack for this solution.
5. Click `Stack Actions` > `create change set`
6. Select `Replace existing template` and `Upload a template file`.
7. Upload the latest template you downloaded in step 1.
8. Click `next`.
9. Leave all parameters the same and click `next`.
10. Check the boxes under `Capabilities` and click `next`.
11. Click `submit`.
12. Once the change set is generated, click `Execute`.

Update the IAM Role in the member accounts.
1. Sign in to the AWS Account in which you deployed the main stack for this solution.
2. Navigate to `CloudFormation` > `StackSets` > `CrowdStrike-Cloud-Security-Stackset`
3. Click `Actions` > `Edit StackSet details`
4. Select `Replace Current Template` and paste the S3 url: https://aws-abi.s3.us-east-1.amazonaws.com/cfn-abi-crowdstrike-fcs/templates/aws_cspm_cloudformation_v2.json
5. Click `Next`
6. Leave all parameters the same and click `next`.
7. Check the box under Capabilities and click `next`.
8. Enter your `AWS OU Id` to define the scope (this should match the scope of your deployment, ie. if you deployed to the root ou `r-******`, enter that same value here).
9. Select the `region` (there should only be one).
10. Click `Next` and Click `Submit`.

## Create change set for bug fixes and other updates

1. Download the latest main template [here](https://raw.githubusercontent.com/aws-ia/cfn-abi-crowdstrike-fcs/main/templates/crowdstrike_init_stack.yaml).
3. Sign in to the AWS Account in which you deployed the main stack for this solution.
3. Navigate to `CloudFormation` > `Stacks`
4. Select the main stack for this solution.
5. Click `Stack Actions` > `create change set`
6. Select `Replace existing template` and `Upload a template file`.
7. Upload the latest template you downloaded in step 1.
8. Click `next`.
9. Leave all parameters the same and click `next`.
10. Check the boxes under `Capabilities` and click `next`.
11. Click `submit`.
12. Once the change set is generated, click `Execute`.

**Next:** Choose [Test the deployment](/test-deployment/index.html).