---
weight: 3
title: Terminologies
description: Terminolgies used in this guide.
---

* **ABI :**  AWS Built-In (ABI).
* **ABI modules :** The GitHub repositories based on AWS Security Reference Architecture (AWS SRA). Provides templates for enabling AWS foundational services such as AWS CloudTrail, Amazon GuardDuty, AWS Security Hub, etc.
* **ABI projects :** The GitHub repositories built by partners in collaboration with AWS. While building these projects, partners use ABI modules to enable AWS services as needed before creating partner-specific assets. The project contains (1) IaC templates to automate enablement of both AWS and partner services, and (2) wrappers for most common formats such as CfCT manifest, SC baselines, and more, so customers can pick and choose from the available services. This solution focuses primarily on including the CfCT manifest file in the package.
* **Assessment:** An individual instance when Horizon compares your cloud settings to the Horizon policies.
* **Assessment schedules:** You can select how frequently your cloud environment is assessed for misconfigurations. You can also exclude AWS services and Regions from assessment.
* **Behavioral:** Patterns of suspicious behavior in your cloud environment.
* **Configuration:** Findings based on policies and benchmarks compared to your cloud configuration.
* **CrowdStrike API client:** CrowdStrike Falcon API client authentication credentials for interaction with CrowdStike APIs via OAuth 2.0 token. Includes an API client ID and API client secret.
* **CrowdStrike event bus:** The AWS event bus in CrowdStrike's environment for receiving events and providing the data to Horizon service.
* **Horizon policies:** A set of rules defined to detect misconfigurations of the cloud resources (IOMs) or to detect suspicious behavior patterns (IOAs).
* **Indicator of attack (IOA):** A pattern of suspicious behavior that suggests an attack might be underway. In Horizon, IOAs are labeled as findings.
* **Indicator of misconfiguration (IOM):** A configuration setting that doesn’t follow recommended security guidelines and might become a security vulnerability in a cloud environment. In Horizon, IOMs are labeled as findings.
* **Registration:** Enroll your AWS account ID with the Horizon service.

**Next:** Choose [Cost and licenses](/costandlicenses/index.html) to get started.
