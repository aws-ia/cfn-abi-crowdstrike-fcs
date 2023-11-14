---
weight: 8
title: Deployment steps
description: Deployment steps.
---

## Launch the CloudFormation template in the AWS Organizations management account {#launch-cfn}


1. Download the [CloudFormation template](https://raw.githubusercontent.com/aws-ia/cfn-abi-crowdstrike-fcs/main/templates/crowdstrike_init_stack.yaml).
2. Launch the CloudFormation template in your [AWS Control Tower home Region](https://docs.aws.amazon.com/controltower/latest/userguide/region-how.html).
    * Stack name: `template-crowdstrike-enable-integrations`
    * Update values of below parameters as needed:
        * **SecretsManagerSecretName**: Type in the Secrets Manager Secret Name that will store the Falcon API Credentials.
        * **Falcon API Client ID**: Type in `Your Falcon OAuth2 Client ID`
        * **Falcon API Secret**: Type in `Your Falcon OAuth2 Client Secret`
        * **CrowdStrike Cloud**: Choose from the available options as needed for your environment. The default is `us1`.
        * **Enable IOA Scanning**: Choose `true` or `false`. The default is `true`
        * **Create Optional Organization CloudTrail**: Choose `true` or `false`. The default is `false`
        * **Provision OUs**: _Comma Delimited List of OU(s) to provision resources. If you are provisioning the entire Organization, please enter the Root OU (r-****)_
        * **Exclude Prohibited Regions**: `[<region-1>, <region-2>,....]`  _(Exclude regions from EventBridge Rules for IOA. Use this when SCPs cause stacksets to fail.)_
        * **Enable Sensor Management**: Choose `true` or `false`. The default is `false`
        * **EnableSSMDistributor**: Choose `true` or `false`. The default is `true`
        * **AutomationAssumeRole**: Define the name of the SSM Automation Execution Role. The default is `crowdstrike-distributor-deploy-role`
        * **ApplyOnlyAtCronInterval**: Choose `true` or `false`. The default is `false`
        * **ScheduleExpression**: Define the schedule or rate by which the SSM Automation runs. The default is `cron(0 0 */1 * * ? *)` (runs every hour)
        * **MaxErrors**: The number or percent of errors that are allowed before the system stops sending requests to run the association on additional targets. The default is `10%`
        * **MaxConcurrency**: The maximum number or percent of targets allowed to run the association at the same time. The default is `20%`

    * Leave the remaining parameters as default (listed below).
        * **Source S3 Bucket Name**: `aws-abi`
        * **S3 Bucket Region**: `us-east-1` 
        * **Staging S3 Key Prefix**: `cfn-abi-crowdstrike-fcs`
        * **Source S3 Bucket Name Prefix**: `cfn-abi-crowdstrike-fcs`
        * **StackSet Execution Role**: `AWSCloudFormationStackSetExecutionRole`
        * **StackSet Administration Role**: `AWSCloudFormationStackSetAdministrationRole`
        * **Organization ID Lambda Function Name**: `abi-crowdstrike-fcs-organization-id`
        * **Organization ID Lambda Role Name**: `abi-crowdstrike-fcs-organization-id-role`

3. Select both of the following capabilities and choose **Submit** to launch the stack.

    [] I acknowledge that AWS CloudFormation might create IAM resources with custom names.

    [] I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND

Wait for the CloudFormation status to change to `CREATE_COMPLETE` state.


## Launch using Customizations for Control Tower {#launch-cfct}


[Customizations for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/) (CfCT) combines AWS Control Tower and other AWS services to help you set up an AWS environment. You can deploy the templates provided with the ABI solution using CfCT.

#### Prerequisites

Create an IAM role with the required permissions in the AWS management account to allow the CfCT solution to launch resources.

#### How it works

To deploy the sample partner integration page, add the following blurb to the `manifest.yaml` file from your CfCT solution and update the account and organizational unit (OU) names as needed.

```yaml
resources:
  - name: deploy-crowdstrike-init-stack
    resource_file: https://aws-abi.s3.us-east-1.amazonaws.com/cfn-abi-crowdstrike-fcs/templates/crowdstrike_init_stack.yaml
    deploy_method: stack_set
    parameters:
      - parameter_key: FalconClientID
        parameter_value: $[alfred_ssm_/crowdstrike/falcon_client_id] # Create SSM parameter with the CrowdStrike API client ID
      - parameter_key: FalconSecret
        parameter_value: $[alfred_ssm_/crowdstrike/falcon_secret] # Create SSM parameter with the CrowdStrike API secret
      - parameter_key: ProvisionOU
        parameter_value: $[alfred_ssm_/crowdstrike/provision-ou] # Create SSM parameter with the OU name
      - parameter_key: ExcludeRegions
        parameter_value: $[alfred_ssm_/crowdstrike/exclude_regions] # Create SSM parameter with regions to exclude
      - parameter_key: SourceS3BucketName
        parameter_value: aws-abi
      - parameter_key: S3BucketRegion
        parameter_value: us-east-1 # Update as needed
      - parameter_key: CreateOrgTrail
        parameter_value: "true" # Update as needed. Set to "false" if you already have an organization trail.
    regions:
      - us-east-1 # Update as needed
    deployment_targets:
      accounts:
        - [[MANAGEMENT-AWS-ACCOUNT-ID]]
```


**Next:** Choose [Post deployment options](/post-deployment-steps/index.html).