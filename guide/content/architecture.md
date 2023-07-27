---
weight: 5
title: Architecture
description: Solution architecture.
---

Deploying this ABI package with default parameters builds the following architecture.

![CSPM Architecture diagram](/images/cspm_architecture.png)

![Sensor Management Architecture diagram](/images/sensor_architecture.png)

As shown in the diagram, the Quick Start sets up the following:

* In all current and AWS accounts in your AWS organization:    
    * IAM Role for CSPM to perform Read-Only activities.
    * IAM Role too allow EventBridge to PutEvents against CrowdStrike's EventBus.
    * EventBridge Rules in each region with CrowdStrike EventBus as target.
    * IAM Role for CrowdStrike to invoke Sensor Management Lambda Function
    * IAM Role for Sensor Management Lambda Function Execution
    * Log Group for Sensor Management Lambda Function
    * Sensor Management Lambda Function

* In the management account:
    * Secrets Manager Secret to store CrowdStrike API Keys.
    * IAM Role for CSPM to perform Read-Only activities.
    * IAM Role for EventBridge to PutEvents against CrowdStrike's EventBus.
    * IAM Role for Lambda Execution.
    * Lambda function to perform account registration with CrowdStrike.
    * Custom CloudFormation Resource to trigger Lambda Function.
    * CloudFormation StackSet to create EventBridge Rules in each region.
    * CloudFormation StackSet to create IAM Roles in member accounts.
    * CloudFormation StackSet to create EventBridge Rules in member accounts.

* In the log archive account:
    * IAM Role for CSPM to perform Read-Only activities.
    * IAM Role to allow EventBridge to PutEvents against CrowdStrike's EventBus.
    * EventBridge Rules in each region with CrowdStrike EventBus as target.

* In the security tooling account:
    * IAM Role for CSPM to perform Read-Only activities.
    * IAM Role to allow EventBridge to PutEvents against CrowdStrike's EventBus.
    * EventBridge Rules in each region with CrowdStrike EventBus as target.

**Next:** Choose [Deployment Options](/deployment-options/index.html) to get started.