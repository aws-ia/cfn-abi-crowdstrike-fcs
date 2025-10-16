---
weight: 100
title: FAQs
description: Frequently asked questions.
---

## When should I use the Sensor Management option?

We recommend this method for deploying the Falcon sensor in AWS environments where AWS Systems Manager (SSM) is in use. After enabling and adding EC2 hosts to the SSM inventory on your registered AWS accounts, you can deploy the Falcon sensor into your EC2 instances from the Falcon console with just one click.

## What is the difference between Sensor Management and SSM Distributor?

Sensor Management (1-Click) allows you to deploy sensors from the Falcon console on demand with a single click. SSM Distributor automatically deploys sensors via scheduled State Manager Associations without requiring manual intervention through the Falcon console.

## How does ECR Registry Connections help secure my container images?

ECR Registry Connections enables CrowdStrike to automatically scan container images stored in your Amazon ECR registries for vulnerabilities and malware. This provides visibility into image security posture before containers are deployed to production environments.

## Does EKS Protection work with existing EKS clusters?

Yes, EKS Protection works with both existing EKS clusters and newly created clusters. When enabled, the solution automatically deploys the Falcon Operator and sensors to existing clusters, and will automatically protect new clusters as they are created.

## What regions are supported for this solution?

This solution can be deployed in any AWS region where the required AWS services (CloudFormation, Lambda, Systems Manager, etc.) are available. For GovCloud deployments, please refer to the GovCloud deployment guide for specific considerations.

## Can I contribute to this repository?

You can submit a GitHub issue if you encounter a problem or want to suggest improvements. To build and contribute a fix or enhancement, submit a GitHub pull request with your changes.

All pull requests go through automatic validations and human reviews before being merged.
