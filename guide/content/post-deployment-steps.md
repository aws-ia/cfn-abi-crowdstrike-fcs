---
weight: 10
title: Postdeployment options
description: Postdeployment options.
---

## Verifying the solution functionality

### Verify account activation in CrowdStrike Falcon console
1. Sign in to the CrowdStrike Falcon console.
2. Navigate to [Cloud-Security > Registration](https://falcon.crowdstrike.com/cloud-security/registration).
3. Verify that each AWS account ID is active in the **Configuration** (IOM), **Behavior** (IOA) and **1-click sensor deployment** columns.
4. After waiting several minutes, choose **Refresh** to retrieve the latest account status.

### Verify SSM Distributor Package deployments in CrowdStrike Falcon console
1. Sign in to the CrowdStrike Falcon console.
2. Navigate to [Host setup and management > Host management](https://falcon.crowdstrike.com/hosts/hosts?navigationFrom=siteNav).
3. Verify that your AWS Instances begin to appear in the host management list with a Host status of "Online".
4. After waiting several minutes, choose **Refresh** to retrieve the latest host status.

**Next:** Choose [Test the deployment](/test-deployment/index.html).