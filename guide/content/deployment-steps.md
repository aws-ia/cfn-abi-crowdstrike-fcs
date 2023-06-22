---
weight: 8
title: Deployment steps
description: Deployment steps.
---


## Launch the CloudFormation template in the AWS management account


1. Download the Cloudformation template from the following location: https://<abi-template-location>
2. Launch the CloudFormation template in your AWS Control Tower home Region.
    * Stack name: `template-crowdstrike-enable-integrations`
    * List parameters with default values and update examples as needed:
        * **EnableIntegrationsStackName**: `template-crowdstrike-enable-integrations`
        * **EnableIntegrationsStackRegion**: `us-east-1`
        * **EnableIntegrationsStackSetAdminRoleName**: `AWSCloudFormationStackSetAdministrationRole`
        * **EnableIntegrationsStackSetExecutionRoleName**: `AWSCloudFormationStackSetExecutionRole`
        * **EnableIntegrationsStackSetExecutionRoleArn**: `arn:aws:iam::<account-id>:role/AWSCloudFormationStackSetExecutionRole`

3. Select both of the following capabilities and choose **Submit** to launch the stack.

    [] I acknowledge that AWS CloudFormation might create IAM resources with custom names.

    [] I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND

Wait for the CloudFormation status to change to `CREATE_COMPLETE` state.


## Launch using Customizations for Control Tower


[Customizations for AWS Control Tower](https://aws.amazon.com/solutions/implementations/customizations-for-aws-control-tower/) (CfCT) combines AWS Control Tower and other AWS services to help you set up an AWS environment. You can deploy the templates provided with the ABI packages using CfCT.

#### Prerequisites

Create an IAM role with the required permissions in the AWS management account to allow the CfCT solution to launch resources.

#### How it works

To deploy the sample partner integration page, add the following blurb to the `manifest.yaml` file from your CfCT solution and update the account and organizational unit (OU) names as needed.

```
resources:
  - name: sra-enable-partner1-solution
    resource_file: https://aws-abi-pilot.s3.us-east-1.amazonaws.com/cfn-abi-aws-reference-guide/templates/abi-enable-partner1-securityhub-integration.yaml
    deploy_method: stack_set
    parameters:
      - parameter_key: pProductArn
        parameter_value: arn:aws:securityhub:us-east-1::product/cloud-custodian/cloud-custodian
      - parameter_key: pSRASourceS3BucketName
        parameter_value: aws-abi-pilot
      - parameter_key: pSRAStagingS3KeyPrefix
        parameter_value: cfn-abi-aws-reference-guide
    deployment_targets:
      accounts:
        - [[MANAGEMENT-AWS-ACCOUNT-ID]]
```


**Next:** Choose [Postdeployment options](/post-deployment-steps/index.html) to get started.