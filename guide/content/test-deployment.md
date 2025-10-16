---
weight: 12
title: Test the deployment
description: Test the deployment
---

## Test Sensor Management
To test the functionality of CrowdStrike Sensor Management, you may discover unmanaged hosts and deploy the sensor.
**Note:** AWS SSM Inventory must be configured in the AWS accounts where you want to enable 1-click sensor deployment. See the AWS article https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-setting-up-ec2.html 

#### Step 1: Discover Unmanaged Hosts
1. In the Falcon console, navigate to **Cloud security > Deployment dashboard**.
2. If the registered cloud accounts contain workloads that don't have a sensor installed, a banner is displayed, stating the number of unprotected hosts. In the banner, click **Take action**.
3. This takes you to the Deploy sensors on unmanaged hosts page.

#### Step 2: Deploy Sensors
1. In the Choose deployment method section, select **Automated**.
2. In the Select hosts section, use the filters to find the hosts where you want to deploy a sensor and select the checkboxes for all hosts where you want to deploy a sensor.
3. Click **Deploy**. A message appears, stating that the sensor is being deployed to hosts.
**Note:** When Automated is selected, this section displays hosts that are part of the SSM inventory and are valid for 1-click sensor deployment. This number may be different from the total number of unmanaged hosts. For the hosts that aren't part of the SSM inventory, use the manual deployment method. For info, see Deploy Sensors Using Ansible.
**Note:** It may take some time for the sensor deployment to complete. 

#### Step 3: Check Deployment Status
1. In the Falcon console, navigate to **Cloud security > Deployment dashboard**.
2. Click **Activity**, next to the dashboard filters.
3. To see a detailed list that you can filter and export, click **View all**. The Deployment activity page displays information about deployments from the past year.

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
