---
weight: 9
title: Deployment steps
description: Deployment steps.
---

## Option 1: Launch the CloudFormation template in the AWS Organizations management account {#launch-cfn}


1. Download the [CloudFormation template](https://raw.githubusercontent.com/aws-ia/cfn-abi-crowdstrike-fcs/main/templates/crowdstrike_init_stack.yaml).
2. Launch the CloudFormation template in your [AWS Control Tower home Region](https://docs.aws.amazon.com/controltower/latest/userguide/region-how.html).
    * Stack name: `template-crowdstrike-enable-integrations`
    * Update the following parameters as needed:
        * Falcon CID Details
            * **Falcon Account Type**: Your Falcon Cloud type.  Allowed values include `commercial` or `govcloud`
            * **Falcon API Client ID**: Your CrowdStrike Falcon API Client ID
            * **Falcon API Secret**: Your CrowdStrike Falcon API Client Secret
            * **CrowdStrike Cloud**: Your Falcon Cloud region.  Allowed values include: `us1`, `us2`, `eu1`, `usgov1`, `usgov2`
            * **Secrets Manager Secret Name**: Name of the Secrets Manager Secret that will store the Falcon API Credentials.
        * AWS Org Details
        **Note:** if `Falcon Account Type` = `govcloud` and `AWS Account Type` = `commercial`, then you must launch this solution in `us-east-1`
            * **AWS Account Type**: Your AWS Cloud type.  Allowed values include `commercial` or `govcloud`
            * **Delegated Administrator Account**: Indicates whether this is a Delegated Administrator account.  Allowed values include `true` or `false`.  Default is `false`
            * **Deployment Scope**: Comma Delimited List of AWS OU(s) to provision. If you are provisioning the entire organization, please enter the Root OU `r-******`
            * **Permissions Boundary Policy Name**: If your Organization requires a PermissionsBoundary policy applied to IAM Roles, enter the **Name** (not the ARN) of your Permissions Boundary policy
        * Sensor Management (1Click)
            * **Enable Sensor Management**
            * **API Credentials Storage Mode**
        * Deploy Falcon Sensors with SSM Distributor
            * **EnableSSMDistributor**: Whether to deploy SSM Associations in each AWS Region to automatically deploy the CrowdStrike Distributor Package against SSM-Managed Ec2 Instances. Allowed values include `true` or `false`. The default is `false`
            * **Document Version**: If EnableSSMDistributor is `true`: Define the version of the CrowdStrike SSM Automation document. The default is `2`.  This value should not change unless advised by CrowdStrike.
            * **SSM Execution Role**: If EnableSSMDistributor is `true`: Define the name of the SSM Automation Execution Role. The default is `crowdstrike-distributor-deploy-role`
            * **Apply Only At Cron Interval**: If EnableSSMDistributor is `true`: Whether to wait for cron interval to initiate SSM Distributor installation.  Allowed values include `true` or `false`. The default is `false`
            * **Cron Schedule Expression**: If EnableSSMDistributor is `true`: Define the schedule or rate by which the SSM Automation runs. The default is `cron(0 0 */1 * * ? *)` (runs every hour)
            * **Max Errors Allowed**: If EnableSSMDistributor is `true`: The number or percent of errors that are allowed before the system stops sending requests to run the association on additional targets. The default is `10%`
            * **Max Concurrency Allowed**: If EnableSSMDistributor is `true`: The maximum number or percent of targets allowed to run the association at the same time. The default is `20%`
        * ECR Registry Connections
            * **Enable ECR Connections for Image Assessment**: Whether to set up ECR Registry Connections for Image Assessments
            * **ECR Execution Role Name**: The name of the role that will be used for Lambda execution.
            * **ECR Lambda Function Name**: The name of the lambda function used to register ECR registry connections.
        * Advanced Configuration Properties
            * **Source S3 Bucket Name**: Name of the S3 Bucket for staging files.  The default is `aws-abi-${AWS::AccountId}-${AWS::Region}`
            * **S3 Bucket Region**: Region of the S3 Bucket for staging files.
            * **Source S3 Bucket Name Prefix**: Prefix of the S3 Bucket for sourcing files. Do not change the default value.
        * EKS Protection
            * **EKSProtection**: Enable CrowdStrike EKS Protection to automatically deploy Falcon Sensor against EKS Clusters. Allowed values include `true` or `false`.  Default is `false`
            * **FalconCID**: Your CrowdStrike Falcon CID with checksum. (eg. ********************************-ab)
            * **DockerAPIToken**: Your Falcon Docker API Token
            * **OrganizationId**: Your AWS Organization ID (eg. o-********)
            * **EventBusName**: Name of the centralized EventBus.  Default is `crowdstrike-eks-eventbus`
            * **EventBridgeRoleName**: Name of the EventBridge IAM role.  Default is `crowdstrike-eks-eventbridge-role`
            * **EKSExecutionRoleName**: Name of the Target Execution IAM role.  Default is `crowdstrike-eks-execution-role`
            * **CodeBuildRoleName**: Name of the CodeBuild IAM role.  Default is `crowdstrike-eks-codebuild-role`
            * **CodeBuildProjectName**: Name of the CodeBuild Project.  Default is `crowdstrike-eks-codebuild`
            * **KubernetesUserName**: Name of the Kubernetes UserName.  Default is `crowdstrike-eks`
            * **Registry**: Source Falcon Image from CrowdStrike or mirror to ECR.  Allowed values are `crowdstrike` or `ecr`.  Default is `crowdstrike`
            * **Backend**: kernel or bpf for Daemonset Sensor.  Allowed Values are `kernel` or `bpf`.  Default is `kernel`
            * **EnableKAC**: Deploy Kubernetes Admission Controller (KAC).  For more info see https://falcon.crowdstrike.com/documentation/page/aa4fccee/container-security#s41cbec3
        

3. Select both of the following capabilities and choose **Submit** to launch the stack.

    [] I acknowledge that AWS CloudFormation might create IAM resources with custom names.

    [] I acknowledge that AWS CloudFormation might require the following capability: CAPABILITY_AUTO_EXPAND

Wait for the CloudFormation status to change to `CREATE_COMPLETE` state.


## Option 2: Launch using Customizations for Control Tower {#launch-cfct}


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
      - parameter_key: SourceS3BucketName
        parameter_value: aws-abi
      - parameter_key: S3BucketRegion
        parameter_value: us-east-1 # Update as needed
    regions:
      - us-east-1 # Update as needed
    deployment_targets:
      accounts:
        - [[MANAGEMENT-AWS-ACCOUNT-ID]]
```


**Next:** Choose [Post deployment options](/post-deployment-steps/index.html).
