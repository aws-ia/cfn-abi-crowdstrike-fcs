---
weight: 10
title: GovCloud Deployment steps
description: GovCloud Deployment steps.
---

## Step 1: Download and prepare the contents of this solution

1. Download the contents of the [GitHub Repo](https://github.com/aws-ia/cfn-abi-crowdstrike-fcs )
2. Navigate to the downloaded directory and run the source_prep.py script
    * `python3 source_prep.py`
3. Confirm the following directory and files were created
    * cfn-abi-crowdstrike-fcs/lambda_functions/packages/codebuild/lambda.zip
    * cfn-abi-crowdstrike-fcs/lambda_functions/packages/cw-helper/lambda.zip
    * cfn-abi-crowdstrike-fcs/lambda_functions/packages/ecr-registration/lambda.zip
    * cfn-abi-crowdstrike-fcs/lambda_functions/packages/eks-existing-clusters/lambda.zip
    * cfn-abi-crowdstrike-fcs/lambda_functions/packages/eks-new-clusters/lambda.zip
    * cfn-abi-crowdstrike-fcs/lambda_functions/packages/register-organization-v2/lambda.zip
    * cfn-abi-crowdstrike-fcs/templates/crowdstrike_init_stack.yaml
    * cfn-abi-crowdstrike-fcs/templates/ecr-registration-stackset.yml
    * cfn-abi-crowdstrike-fcs/templates/eks-eventbridge-stackset.yml
    * cfn-abi-crowdstrike-fcs/templates/eks-protection-stack.yml
    * cfn-abi-crowdstrike-fcs/templates/eks-root-roles.yml
    * cfn-abi-crowdstrike-fcs/templates/eks-target-roles-stackset.yml
    * cfn-abi-crowdstrike-fcs/templates/ssm-association-stackset.yml
    * cfn-abi-crowdstrike-fcs/templates/ssm-setup-stackset.yml

## Step 2: Upload prepared contents to your S3 Bucket

1. In your AWS Console, navigate to the root of an S3 bucket
2. Click **Upload**
3. Click **Add Folder**
4. Select the new `cfn-abi-crowdstrike-fcs` directory.
    * **Note**:  this directory may have the same name of the repo you downloaded.  Please ensure you are selecting the `cfn-abi-crowdstrike-fcs` directory which contains only the folders and files created by the source_prep.py script in the previous step.
5. Click **Upload**

## Step 3: Launch the CloudFormation template in the AWS Organizations management account {#launch-cfn}

1. Launch the CloudFormation template in your [AWS Control Tower home Region](https://docs.aws.amazon.com/controltower/latest/userguide/region-how.html).
    * Stack name: `template-crowdstrike-enable-integrations`
    * Update the following parameters as needed:
        * Falcon CID Details
            * **Falcon Account Type**: Your Falcon Cloud type.  Select `govcloud`
            * **Falcon API Client ID**: Your CrowdStrike Falcon API Client ID
            * **Falcon API Secret**: Your CrowdStrike Falcon API Client Secret
            * **CrowdStrike Cloud**: Your Falcon Cloud region.  Allowed values include: Select `usgov1` or `usgov2`
            * **Secrets Manager Secret Name**: Name of the Secrets Manager Secret that will store the Falcon API Credentials.
        * AWS Org Details
            * **AWS Account Type**: Your AWS Cloud type.  Select `govcloud`
            * **Delegated Administrator Account**: Indicates whether this is a Delegated Administrator account.  Allowed values include `true` or `false`.  Default is `false`
            * **Deployment Scope**: Comma Delimited List of AWS OU(s) to provision. If you are provisioning the entire organization, please enter the Root OU `r-******`
            * **Permissions Boundary Policy Name**: If your Organization requires a PermissionsBoundary policy applied to IAM Roles, enter the **Name** (not the ARN) of your Permissions Boundary policy
        * Deploy Falcon Sensors with SSM Distributor  **Skip, this is not supported in GovCloud yet**
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

        * **Important**
        * Advanced Configuration Properties
            * **Source S3 Bucket Name**: Name of the S3 Bucket you used to upload the contents.
            * **S3 Bucket Region**: Region in which this S3 Bucket resides. ie. `us-gov-west-1` or `us-gov-east-1`
            * **Source S3 Bucket Name Prefix**: Prefix of the S3 Bucket for sourcing files. Do not change the default value.
        * EKS Protection **Skip, this is not supported in GovCloud yet**
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


**Next:** Choose [Post deployment options](/post-deployment-steps/index.html).
