---
weight: 100
title: FAQs
description: Frequently asked questions.
---

## What is the difference between 1-Click and SSM Distributor?

1-Click allows you to deploy sensors from the Falcon console on demand with a single click, which can be enabled via the Falcon Console. SSM Distributor automatically deploys sensors via scheduled State Manager Associations without requiring manual intervention through the Falcon console.

## How does ECR Registry Connections help secure my container images?

ECR Registry Connections enables CrowdStrike to automatically scan container images stored in your Amazon ECR registries for vulnerabilities and malware. This provides visibility into image security posture before containers are deployed to production environments.

## Does EKS Protection work with existing EKS clusters?

Yes, EKS Protection works with both existing EKS clusters and newly created clusters. When enabled, the solution automatically deploys the Falcon Operator and sensors to existing clusters, and will automatically protect new clusters as they are created.

## What regions are supported for this solution?

This solution can be deployed in any AWS region where the required AWS services (CloudFormation, Lambda, Systems Manager, etc.) are available. For GovCloud deployments, please refer to the GovCloud deployment guide for specific considerations.

SSM Distributor is enabled for most regions, for an updated list please see https://github.com/CrowdStrike/aws-ssm-distributor

EKS Protection is not yet supported by GovCloud

## Can I contribute to this repository?

You can submit a GitHub issue if you encounter a problem or want to suggest improvements. To build and contribute a fix or enhancement, submit a GitHub pull request with your changes.

All pull requests go through automatic validations and human reviews before being merged.
