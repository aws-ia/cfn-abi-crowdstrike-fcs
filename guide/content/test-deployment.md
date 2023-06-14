---
weight: 10
title: Test the deployment
description: Test the deployment.
---

To test Horizon functionality, you can generate findings by intentionally violating a policy of your choice.
**Note:** CrowdStrike does not recommend running these steps against any accounts and/or workloads with sensitive data.

## Step 1: Review policies.
* Log in to the CrowdStrike Falcon console.
* Navigate to **Cloud Security > Cloud Security Posture > Policies**.
* Filter by AWS and choose a service.
* Review Configuration and Behavioral policies.

## Step 2: Execute policy violation.
* Choose a policy to test, for example **VPC Flow Logs Disabled**.
* Make the relevant change in your AWS account.

## Step 3:
* Navigate to **Cloud Security > Cloud Security Posture > Assessment**, and review your Horizon assessment findings.
* If the policy is Behavioral, wait a few minutes for the finding to appear.
* If the policy is Configuration, wait for the next assessment scan for the finding to appear. Two hours is the default interval, but you can change this setting by navigating to **Cloud Security > Cloud Security Posture > Settings**.


**Next:** Choose [Additonal resources](/additional-resources/index.html) to get started.