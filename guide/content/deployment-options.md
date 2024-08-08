---
weight: 6
title: Deployment options
description: Deployment options.
---

#### Deployment options supported by this ABI solution

The following deployment options are supported by this ABI solution:

* Launch the [CloudFormation template in the AWS Management Console](/deployment-steps/index.html#launch-cfn).
* Launch using [Customizations for AWS Control Tower (CfCT)](/deployment-steps/index.html#launch-cfct).

####  Cloud types supported by this solution

You may use this solution to register the following account types:

* Register Commercial AWS Accounts with Commercial Falcon (us1, us2, eu1)
* Register Commercial AWS Accounts with GovCloud Falcon (usgov1, usgov2)
* Register GovCloud AWS Accounts with GovCloud Falcon (usgov1, usgov2)

**Note:** When registering Commercial AWS with GovCloud Falcon, this solution **must be launched in us-east-1**

#### Optional CloudTrail

This solution can deploy a CloudTrail for you AWS Organization.

* Create Default Organization CloudTrail: This optional trail is required if you do not have an Organization CloudTrail enabled for you AWS Organization.

**Next:** Choose [Predeployment steps](/pre-deployment-steps/index.html).
