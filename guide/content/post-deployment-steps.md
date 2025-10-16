---
weight: 11
title: Postdeployment options
description: Postdeployment options.
---

## Verifying the solution functionality

### Verify account activation in CrowdStrike Falcon console
1. Sign in to the CrowdStrike Falcon console.
2. Navigate to [Cloud-Security > Registration](https://falcon.crowdstrike.com/cloud-security/registration).
3. Verify that each AWS account ID is active in the **1-click sensor deployment** column.
4. After waiting several minutes, choose **Refresh** to retrieve the latest account status.

### Verify SSM Distributor Package deployments in CrowdStrike Falcon console
1. Sign in to the CrowdStrike Falcon console.
2. Navigate to [Host setup and management > Host management](https://falcon.crowdstrike.com/hosts/hosts?navigationFrom=siteNav).
3. Verify that your AWS Instances begin to appear in the host management list with a Host status of "Online".
4. After waiting several minutes, choose **Refresh** to retrieve the latest host status.

### Verify ECR Registry Connections in CrowdStrike Falcon console
1. Sign in to the CrowdStrike Falcon console.
2. Navigate to [Cloud Security > Image Assessment > Registry Connections](https://falcon.crowdstrike.com/cloud-security/image-assessment/registry-connections).
3. Verify that your AWS ECR registries appear in the registry connections list with a Status of "Connected".
4. After waiting several minutes, choose **Refresh** to retrieve the latest registry status.

### Verify EKS Protection deployments in CrowdStrike Falcon console
If you enabled EKS Protection:
1. Sign in to the CrowdStrike Falcon console.
2. Navigate to [Cloud Security > Kubernetes Protection > Clusters](https://falcon.crowdstrike.com/cloud-security/kubernetes-protection/clusters).
3. Verify that your EKS clusters appear with sensors deployed.
4. After waiting several minutes, choose **Refresh** to retrieve the latest cluster status.

## Create change set for bug fixes and other updates

1. Download the latest main template [here](https://raw.githubusercontent.com/aws-ia/cfn-abi-crowdstrike-fcs/main/templates/crowdstrike_init_stack.yaml).
2. Sign in to the AWS Account in which you deployed the main stack for this solution.
3. Navigate to `CloudFormation` > `Stacks`
4. Select the main stack for this solution.
5. Click `Stack Actions` > `create change set`
6. Select `Replace existing template` and `Upload a template file`.
7. Upload the latest template you downloaded in step 1.
8. Click `next`.
9. Leave all parameters the same and click `next`.
10. Check the boxes under `Capabilities` and click `next`.
11. Click `submit`.
12. Once the change set is generated, click `Execute`.

**Next:** Choose [Test the deployment](/test-deployment/index.html).
