---
weight: 6
title: Architecture
description: Solution architecture.
---

Deploying this ABI solution with default parameters builds the following architecture.

### Sensor Management (OneClick)
![Sensor Management Architecture diagram](/images/sensor_architecture.png)  

### SSM Distributor
![SSM Distributor Architecture diagram](/images/distributor_architecture.png)  
* In the child AWS accounts:
    * Secrets Manager Secret to manage CrowdStrike API Credentials.
    * IAM role that allows SSM Associations to retrieve API Credentials from Secrets Manager.
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

### ECR Registry Connections
* If you enable ECR Registry Connections:
    * In the primary region of all child accounts:
        * IAM Role for ECR Registry Connection Scanning
        * Lambda Function to register each AWS Region with Registry Connection Service
        * IAM Role for Lambda Execution
        * Secret for storing Falcon API Credentials

**Next:** Choose [Deployment options](/deployment-options/index.html).
