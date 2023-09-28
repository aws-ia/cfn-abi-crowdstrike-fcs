---
weight: 10
title: Test the deployment
description: Test the deployment
---

## Test CSPM 
To test the functionality of CrowdStrike Falcon CSPM, you may generate findings by intentionally violating a policy of your choice.
**Note:** CrowdStrike does not recommend running these steps against any accounts and/or workloads with sensitive data.

## Step 1: Review policies.
1. Log in to the CrowdStrike Falcon console.
2. Navigate to **Cloud Security > Cloud Security Posture > Policies**.
3. Filter by AWS and choose a service.
4. Review Configuration and Behavioral policies.

## Step 2: Execute Policy Violation
1. Choose a policy to test, for example **VPC Flow Logs Disabled**.
2. Make the relevant change in your AWS account.

## Step 3
1. Navigate to **Cloud Security > Cloud Security Posture > Assessment**, and review your assessment findings.
2. If the policy is Behavioral, wait a few minutes for the finding to appear.
3. If the policy is Configuration, wait for the next assessment scan for the finding to appear. Two hours is the default interval, but you can change this setting by navigating to **Cloud Security > Cloud Security Posture > Settings**.

## Test Sensor Management
To test the functionality of CrowdStrike Sensor Management, you may discover unmanaged hosts and deploy the sensor.
**Note:** AWS SSM Inventory must be configured in the AWS accounts where you want to enable 1-click sensor deployment. See the AWS article https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-setting-up-ec2.html 

## Step 1: Discover Unmanaged Hosts
1. In the Falcon console, navigate to **Cloud security > Deployment dashboard**.
2. If the registered cloud accounts contain workloads that don't have a sensor installed, a banner is displayed, stating the number of unprotected hosts. In the banner, click **Take action**.
3. This takes you to the Deploy sensors on unmanaged hosts page.

## Step 2: Deploy Sensors
1. In the Choose deployment method section, select **Automated**.
2. In the Select hosts section, use the filters to find the hosts where you want to deploy a sensor and select the checkboxes for all hosts where you want to deploy a sensor.
3. Click **Deploy**. A message appears, stating that the sensor is being deployed to hosts.
**Note:** When Automated is selected, this section displays hosts that are part of the SSM inventory and are valid for 1-click sensor deployment. This number may be different from the total number of unmanaged hosts. For the hosts that aren't part of the SSM inventory, use the manual deployment method. For info, see Deploy Sensors Using Ansible.
**Note:** It may take some time for the sensor deployment to complete. 

## Step 3: Check Deployment Status
1. In the Falcon console, navigate to **Cloud security > Deployment dashboard**.
2. Click **Activity**, next to the dashboard filters.
3. To see a detailed list that you can filter and export, click **View all**. The Deployment activity page displays information about deployments from the past year.

**Next:** Choose [Additonal Resources](/additional-resources/index.html) to get started.