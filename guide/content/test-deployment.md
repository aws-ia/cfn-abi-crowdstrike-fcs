---
weight: 10
title: Test the deployment
description: Test the deployment
---

To test the functionality of CrowdStrike Falcon Horizon, you may generate findings by intentionally violating a policy of your choice.
**Note:** CrowdStrike does not recommend executing these steps against any accounts and/or workloads with sensitive data.

## Step-1: Review Policies
* Log in to the CrowdStrike Falcon console
* Navigate to Cloud Security/Cloud Security Posture/Policies
* Filter by AWS and choose a service
* Review Configuration and Behavioral policies.

## Step-2: Execute Policy Violation
* Choose a policy to test, for example "VPC Flow Logs Disabled"
* Make the relevant change in your AWS account

## Step-3
* Review your Horizon Assessment findings in Cloud Security/Cloud Security Posture/Assessment
* If the policy you chose is Behavioral, please wait a few minutes for the finding to appear.
* If the policy you chose is Configuration, please wait for the next assessment scan for the finding to appear.  2 hours is the default interval, but this may be changed in Cloud Security/Cloud Security Posture/Settings


**Next:** Choose [Additonal Resources](/additional-resources/index.html) to get started.