# CrowdStrike Built-In

## 1. Prerequisite: Create Falcon API Keys
1. Login to Falcon console
2. Navigate to Support and resources > API clients and keys
3. Add new API Client
4. Enable Scope: CSPM Registration Read & Write
5. Once added, save Client ID and Client Secret
6. Make note of Base URL (will determine parameter CSCLoud)

## 2. Upload templates to S3
1. Make note of S3 bucket, key prefix & region 

## 3. Create CFN Stack from horizon_init_stack.yaml with parameters:
1. FalconClientID: from step 1e
2. FalconSecret: from step 1e
3. CSCloud: us-1, us-2 or eu-1 (from step 1f)
4. EnableIOA: choose whether to include behavioral Indicators of Attack (will launch Event bridge rules to forward events to CrowdStrike Horizon)
5. StackSetAdminRole: if EnableIOA = true, what to name StackSetAdminRole for self-managed EB Stacksets in root account
6. StackSetExecRole: if EnableIOA = true, what to name StackSetAdminRole for self-managed EB Stacksets in root account
7. S3BucketName: bucketname where templates are stored
8. S3BucketRegion: bucket region where templates are stored
9. S3KeyPrefix: object key prefix where templates are stored

## 4. Verify Stack completes and check Falcon Console AWS Account Registration
1. Navigate to Cloud Security > Account Registration
2. After a few minutes you will see all org account ids listed, which means they are registered with Falcon Horizon, but not necessarily provisioned yet with necessary resources
3. At this point the org account will show Configuration (IOM) Active, Behavior (IOA) Inactive

## 5. Enable IOM in child accounts/ous
1. Navigate to Cloudformation > StackSets
2. Select CrowdStrike-Horizon-Stackset and Add Stacks
3. Choose Entire Org (or specific OUs if desired)
4. Only choose one region
5. Verify stack operations complete and check Falcon Console AWS Account Registration
6. At this point the child accounts will show Configuration (IOM) Active, Behavior (IOA) Inactive

## 6. Enable IOA in Org Account (if EnableIOA = false, skip this step)
1. Navigate to Cloudformation > StackSets
2. Select crowdStrike-Horizon-Root-EB-Stackset and Add Stacks
3. Run stacks in this account against at least one region (include all regions with running workloads if any)
4. Make sure the StackSet Administration and StackSet Execution Roles match what you selected in the parameters in step 3e and 3f
5. Verify stack operations complete and check Falcon Console AWS Account Registration
6. At this point the org account will show Configuration (IOM) Active, Behavior (IOA) Active

## 7. Enable IOA in child accounts/ous (if EnableIOA = false, skip this step)
1. Navigate to Cloudformation > StackSets
2. Select CrowdStrike-Horizon-EB-Stackset and Add Stacks
3. Choose Entire Org (or specific OUs if desired)
4. Choose at least one region (include all regions with running workloads if any)
5. Verify stack operations complete and check Falcon Console AWS Account Registration
6. At this point the child accounts will show Configuration (IOM) Active, Behavior (IOA) Active
