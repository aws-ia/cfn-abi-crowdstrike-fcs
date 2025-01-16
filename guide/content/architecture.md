---
weight: 6
title: Architecture
description: Solution architecture.
---

Deploying this ABI solution with default parameters builds the following architecture.

### CSPM Architecture
![CSPM Architecture diagram](/images/cspm_architecture.png)  
### Sensor Management (OneClick)
![Sensor Management Architecture diagram](/images/sensor_architecture.png)  

* In all current accounts in your AWS organization:
    * IAM role that allows CrowdStrike to perform read-only activities.
    * IAM role that allows Amazon EventBridge to perform PutEvents actions against CrowdStrike's event bus.
    * EventBridge rules in each Region with CrowdStrike event bus as the target.
    * IAM Role for CrowdStrike to invoke Sensor Management Lambda Function
    * IAM Role for Sensor Management Lambda Function Execution
    * Log Group for Sensor Management Lambda Function
    * Sensor Management Lambda Function

* In the management account:
    * IAM role that allows CrowdStrike to perform read-only activities.
    * IAM role that allows EventBridge to perform PutEvents actions against CrowdStrike's event bus.
    * IAM role for running the AWS Lambda function.
    * In the primary Region, AWS Secrets Manager secret for storing CrowdStrike API keys and a Lambda function to perform account registration with CrowdStrike.
    * EventBridge rules in both primary and additional Regions.
    * A custom AWS CloudFormation resource to trigger the Lambda function.
    * AWS CloudFormation StackSets to create EventBridge rules in each Region and to create IAM roles and EventBridge rules in member accounts.

* In the child AWS accounts (log archive and security tooling accounts):
    * EventBridge rules in each Region with CrowdStrike event bus as the target.
    * IAM role that allows CrowdStrike to perform read-only activities.
    * IAM role that allows EventBridge to perform PutEvents actions against CrowdStrike's event bus.
    * Secrets Manager Secret to manage CrowdStrike API Credentials.
    * IAM role that allows SSM Associations to retrive API Credentials from Secrets Manager.
    * SSM Associations to deploy Falcon Sensor via SSM Distributor Package against SSM-Managed instances.

### SSM Distributor
![SSM Distributor Architecture diagram](/images/distributor_architecture.png)  
* In the child AWS accounts:
    * Secrets Manager Secret to manage CrowdStrike API Credentials.
    * IAM role that allows SSM Associations to retrive API Credentials from Secrets Manager.
    * SSM Associations to deploy Falcon Sensor via SSM Distributor Package against SSM-Managed instances.

### EKS Protection
![EKS Protection Diagram](/images/eks-protect-diagram.png)  
* If you enable EKS Protection:
    * In the centralized account:
        * IAM Role for EventBridge to trigger Lambda
        * IAM Role for Lambda Execution
        * IAM Role for CodeBuild Execution
        * EventBus to receive cluster events
        * EventBridge Rule to trigger Lambda
        * Lambda functions to process cluster events and trigger Codebuild
        * CodeBuild project to apply Falcon Operator to EKS Clusters
        * Secret to store Falcon API key
        * Optional ECR repositories if registry = ecr
        * VPC, NAT, EIP for CodeBuild project
    * In the child accounts:
        * IAM Role for EventBridge to trigger Lambda
        * IAM Role for Lambda Execution
        * IAM Role for CodeBuild Execution
        * EventBridge Rule to send cluster events to centralized EventBus

**Next:** Choose [Deployment options](/deployment-options/index.html).