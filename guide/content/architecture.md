---
weight: 5
title: Architecture
description: Solution architecture.
---

Deploying this ABI solution with default parameters builds the following architecture.

![Architecture diagram](/images/abi-crowdstrike-architecture-diagram.png)

As shown in the diagram, the solution sets up the following:

* In all current Horizon accounts in your AWS organization:
    * IAM role that allows Horizon to perform read-only activities.
    * IAM role that allows Amazon EventBridge to perform PutEvents actions against CrowdStrike's event bus.
    * EventBridge rules in each Region with CrowdStrike event bus as the target.

* In the management account:
    * IAM role that allows Horizon to perform read-only activities.
    * IAM role that allows EventBridge to perform PutEvents actions against CrowdStrike's event bus.
    * IAM role for running the AWS Lambda function.
    * In the primary Region, AWS Secrets Manager secret for storing CrowdStrike API keys and a Lambda function to perform account registration with CrowdStrike.
    * EventBridge rules in both primary and additional Regions.
    * A custom AWS CloudFormation resource to trigger the Lambda function.
    * AWS CloudFormation StackSets to create EventBridge rules in each Region and to create IAM roles and EventBridge rules in member accounts.

* In the child AWS accounts (log archive and security tooling accounts):
    * EventBridge rules in each Region with CrowdStrike event bus as the target.
    * IAM role that allows Horizon to perform read-only activities.
    * IAM role that allows EventBridge to perform PutEvents actions against CrowdStrike's event bus.

**Next:** Choose [Deployment options](/deployment-options/index.html).