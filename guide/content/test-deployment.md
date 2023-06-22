---
weight: 10
title: Test the deployment
description: Test the deployment.
---

To test Horizon functionality, you can generate findings by intentionally violating a policy of your choice.
**Note:** CrowdStrike does not recommend running these steps against any accounts and/or workloads with sensitive data.

## Step 1: Review policies.
1. Log in to the CrowdStrike Falcon console.
2. Navigate to **Cloud Security > Cloud Security Posture > Policies**.
3. Filter by AWS and choose a service.
4. Review Configuration and Behavioral policies.

## Step 2: Test for policy violation.
1. Choose a policy to test, for example **VPC Flow Logs Disabled**.
2. Make the relevant change in your AWS account.

## Step 3: Review assessment findings.
1. Navigate to **Cloud Security > Cloud Security Posture > Assessment**, and review your Horizon assessment findings.
2. If the policy is Behavioral, wait a few minutes for the finding to appear.
3. If the policy is Configuration, wait for the next assessment scan for the finding to appear. Two hours is the default interval, but you can change this setting by navigating to **Cloud Security > Cloud Security Posture > Settings**.


**Next:** Choose [Additonal resources](/additional-resources/index.html) to get started.