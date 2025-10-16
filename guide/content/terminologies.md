---
weight: 3
title: Terminologies
description: Terminolgies used in this guide.
---

* **ABI :**  AWS Built-In (ABI).
* **ABI modules :** The GitHub repositories based on [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html) (AWS SRA). Modules provide templates for enabling AWS foundational services such as AWS CloudTrail, Amazon GuardDuty, AWS Security Hub, etc.
* **ABI solutions :** The GitHub repositories built by partners in collaboration with AWS. While building these solution, partners use ABI modules to enable AWS services as needed before creating partner-specific assets. The solution contains (1) Infrastructure as Code (IaC) templates to automate enablement of both AWS and partner services, and (2) wrappers for most common formats such as CfCT manifest, AWS Service Catalog baselines, and more, so customers can pick and choose from the available services.
* **CrowdStrike API client:** CrowdStrike Falcon API client authentication credentials for interaction with CrowdStike APIs via OAuth 2.0 token. Includes an API client ID and API client secret.
* **CrowdStrike event bus:** The AWS event bus in CrowdStrike's environment for receiving events from EKS clusters and providing runtime protection data to CrowdStrike.
* **ECR Registry Connections:** Integration that enables CrowdStrike to assess container images stored in Amazon Elastic Container Registry (ECR) for vulnerabilities and malware.
* **EKS Protection:** Runtime security monitoring for Amazon Elastic Kubernetes Service clusters that detects suspicious activities and provides visibility into containerized workloads.
* **Registration:** Enroll your AWS account ID with the CrowdStrike service to enable integrations across your AWS environment.
* **Sensor Management:** Enable 1-click sensor deployment to quickly and easily deploy the Falcon sensor to your cloud workloads. Use the Deployment dashboard to discover unmanaged AWS hosts and unregistered AWS accounts and to kick start workflows to register your cloud accounts and automate sensor deployments.
* **SSM Distributor:** Install the Falcon sensor on instances across your AWS accounts using AWS SSM State Manager Associations.  

**Next:** Choose [Cost and licenses](/costandlicenses/index.html).
