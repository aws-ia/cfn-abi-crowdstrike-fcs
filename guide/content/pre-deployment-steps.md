---
weight: 8
title: Predeployment steps
description: Predeployment steps.
---

Before deploying this ABI solution, complete the following steps:

1. Subscribe to the [CrowdStrike Falcon Cloud Security](https://aws.amazon.com/marketplace/pp/prodview-l6ti2ml2i2g6y?ref_=esp&feature_=FeaturedProducts) AWS Marketplace listing.
2. Create Crowdstrike API Client in Falcon UI with the following scope: 
- Sensor management: Read and Write (If Sensor Management enabled)
- Installation Tokens: Read, Sensor Download: Read (If Sensor Management or SSM Distributor enabled)
- ECR Registry Scanning: Read and Write (If ECR Registry Connections enabled)
- Falcon Images Download: Read (If EKS Protection enabled)
- Sensor Download: Read (If EKS Protection enabled)
3. Become familiar with the [additional resources](/additional-resources/index.html) later in this guide.

**Next:** Choose [Deployment steps](/deployment-steps/index.html).
