---
weight: 100
title: FAQs
description: Frequently asked questions.
---

## How frequently will CrowdStrike Cloud Security scan my environment for Configuration (IOM) assessment?

You can configure your settings to determine the frequency of assessments. The default rate is two hours after the last successful assessment. Optional intervals are six, 12, and 24 hours.

## How frequently will CrowdStrike Cloud Security scan my environment for Behavioral (IOA) assessment?

Indicator of Attack (IOA) findings are not generated by scheduled scans, but instead are forwarded to CrowdStrike at the time of the event via EventBridge. IOA findings will appear in your Falcon console in near real time.

## Can I create custom policies with CrowdStrike Falcon Cloud Security?

You can create custom policies for misconfiguration detections in your cloud accounts in the Falcon console. By defining your own rules, you get more coverage with fine-tuned policies that meet your own security and compliance requirements.

## When should I use the Sensor Management option?

We recommend this method for deploying the Falcon sensor in AWS environments where AWS Systems Manager (SSM) is in use. After enabling and adding EC2 hosts to the SSM inventory on your registered AWS accounts, you can deploy the Falcon sensor into your EC2 instances from the Falcon console with just one click.

## Can I contribute to this repository?

You can submit a GitHub issue if you encounter a problem or want to suggest improvements. To build and contribute a fix or enhancement, submit a GitHub pull request with your changes.

All pull requests go through automatic validations and human reviews before being merged.



