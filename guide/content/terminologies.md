---
weight: 3
title: Terminologies
description: Terminolgies used in this guide.
---

* **ABI :**   AWS Built In (ABI)  as explained above.
* **ABI Modules :** The GitHub repositories based of AWS SRA, which provide templates for enabling AWS foundational services like CloudTrail, GuardDuty, SecurityHub and more security services.
* **ABI Projects :** The GitHub repositories built by Partners in partnership with AWS. While building these projects, partners leverage ABI Modules provided to enable AWS services as needed before creating partner specific assets. The project contains 1\ IaC templates to automate enablement of both AWS and Partner services, 2\ Wrappers for most common formats like CfCT manifest, SC Baselines and more to allow customers to easily pick and choose from the services available. For Pilot, we will focus only on including CfCT manifest file in the package.
* **Assessment:** An individual instance when CSPM compares your cloud settings to the CSPM policies.
* **Assessment Schedules:** You can select how frequently your cloud environment is assessed for misconfigurations. You can also exclude AWS services and regions from assessment.
* **Behavioral:** Patterns of suspicious behavior in your cloud environment. 
* **Configuration:** Findings based on policies and benchmarks compared to your cloud configuration. 
* **CrowdStrike API Client:** CrowdStrike Falcon API Client authentication credentials for interaction with CrowdStike APIs via OAuth 2.0 token.  Includes an API Client ID and API Client Secret.
* **CrowdStrike EventBus:** The AWS EventBus in CrowdStrike's environment to receive events and provide the data to CrowdStrike Falcon CSPM service.
* **CSPM Policies:** CSPM policies are a set of rules defined to detect misconfigurations of the cloud resources (IOMs) or to detect suspicious behavior patterns (IOAs). 
* **Indicator of attack (IOA):** A pattern of suspicious behavior that suggests an attack might be underway. In CSPM, IOAs are labeled as findings.
* **Indicator of misconfiguration (IOM):** A configuration setting that doesn’t follow recommended security guidelines and might become a security vulnerability in a cloud environment. In CSPM, IOMs are labeled as findings.
* **Registration:** Enroll your AWS Account ID with CrowdStrike Falcon CSPM service.
* **Sensor Management:** Enable 1-click sensor deployment to quickly and easily deploy the Falcon sensor to your cloud workloads. Use the Deployment dashboard to discover unmanaged AWS hosts and unregistered AWS accounts and to kick start workflows to register your cloud accounts and automate sensor deployments.

**Next:** Choose [Cost and licenses](/costandlicenses/index.html) to get started.
