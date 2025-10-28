---
weight: 5
title: How it Works
description: How each service in this solution works.
---

### SSM Distributor
If your AWS environment uses AWS Systems Manager (SSM), you can leverage it to deploy the Falcon sensor to your EC2 instances automatically via State Manager Associations.  The same CrowdStrike Falcon Distributor Package that enables 1Click, can also be deployed against instances in your environment without clicking through the Falcon Console.  See [GitHub Documentation](https://github.com/CrowdStrike/aws-ssm-distributor/blob/main/README.md) for details. 

This solution allows you to easily set up the necessary State Manager Associations in each region of each account in the AWS Organization.

This is accomplished by
1. IAM Role in each account to provide execution role for State Manager Assocations
2. State Manager Association in each region of each account to execute the CrowdStrike Falcon Distributor package against SSM Managed EC2 instances.  The Association can be configured with a schedule and will handle both Linux and Windows machines.
3. Secrets Manager Secret in each region of each account to store Falcon API Credentials for the CrowdStrike Falcon Distributor package.

**Note:** This feature will only apply to SSM-Managed EC2 Instances.  See [AWS Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-setting-up-ec2.html) for details.

### EKS Protection
If your AWS environment uses EKS to run Kubernetes workloads, you can automatically deploy the Falcon Operator and Falcon sensor to each EKS Cluster.  This solution will automically deploy Falcon to existing clusters as well as new clusters upon creation.

This is accomplished by
1. IAM Roles in each account to provide permissions to List Clusters and create EKS Access Entries.
2. EventBridge rules in each region of each account to trigger on CreateCluster events.
3. IAM Roles in root account to facilitate permissions for EventBridge, Lambda and CodeBuild.
4. Lambda function to list EKS clusters and invoke codebuild for initial deployment of Falcon to existing clusters.
5. Lambda function to be triggered by CreateCluster and invoke codebuild against new clusters.
6. CodeBuild project to update access entries, pull CrowdStrike images and deploy Falcon Operator/Sensor.

### ECR Registry Connections
Ensuring that the images in the registry are assessed for vulnerabilities before runtime is an important part of cloud workload protection.  When a new registry connection is added, a job starts to discover all the repositories, and in parallel, the images and tags are collected from each repository to create the catalog. The catalog contains info about all images, the repository they come from, the image tag associated with that image, and the registry it belongs to. The catalog is used to compare the future and current state of the repo. We avoid showing duplicate image info by using the catalog info, including when tags move between images, to determine if we have already seen and assessed an image. When a catalog is created for a registry, the images in the catalog are inventoried.

This is accomplished by
1. IAM Roles in each account to provide permissions to push images to CrowdStrike Falcon.
2. Lambda function in each account to register ECR Registries with Registry Connection service.

**Note:** This will connect registries in each AWS Account of the org, for each region.


**Next:** Choose [Architecture](/architecture/index.html).
