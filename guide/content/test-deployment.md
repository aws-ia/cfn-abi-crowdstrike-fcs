---
weight: 12
title: Test the deployment
description: Test the deployment
---

## Test SSM Distributor
To test the functionality of SSM Distributor sensor deployment:

#### Step 1: Verify SSM Associations
1. In the AWS Console, navigate to **AWS Systems Manager > Node Management > State Manager**.
2. Verify that the CrowdStrike Falcon Distributor associations are present and have successfully executed.
3. Check the association execution history to ensure successful deployments.

#### Step 2: Verify Host Registration
1. In the Falcon console, navigate to **Host setup and management > Host management**.
2. Verify that your AWS EC2 instances appear in the host management list with a Host status of "Online".
3. Check that the sensor version and last seen timestamp are recent.

## Test ECR Registry Connections
To test the functionality of ECR Registry Connections:

#### Step 1: Verify Registry Connection
1. In the Falcon console, navigate to **Cloud Security > Image Assessment > Registry Connections**.
2. Verify that your AWS ECR registries appear with a Status of "Connected".
3. Check that the last scanned timestamp is recent.

#### Step 2: Push a Test Image
1. Push a container image to one of your connected ECR repositories.
2. Wait a few minutes for the image to be scanned.
3. Navigate to **Cloud Security > Image Assessment > Images** to verify the image appears and has been assessed.

## Test EKS Protection
To test the functionality of EKS Protection (if enabled):

#### Step 1: Create a Test EKS Cluster
1. Create a new EKS cluster in one of your AWS accounts.
2. Wait for the cluster creation event to trigger the automated deployment process.

#### Step 2: Verify Sensor Deployment
1. In the Falcon console, navigate to **Cloud Security > Kubernetes Protection > Clusters**.
2. Verify that your EKS cluster appears with sensors deployed.
3. Check that the cluster status shows as protected.

#### Step 3: Verify Existing Clusters
1. For existing EKS clusters, verify they also appear in the Kubernetes Protection dashboard.
2. Check that the Falcon Operator and sensors have been deployed to existing clusters.

**Next:** Choose [Additional Resources](/additional-resources/index.html) to get started.
