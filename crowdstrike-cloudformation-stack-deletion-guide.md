# CrowdStrike CloudFormation Stack Deletion Guide

## ⚠️ CRITICAL WARNING

**Deleting the CrowdStrike CloudFormation stack created by `crowdstrike_init_stack.yaml` will completely deregister your AWS Organization from Falcon Cloud Security.** This action will:

- **Remove all security monitoring** across your entire AWS Organization
- **Disable real-time threat detection** (IOA - Indicators of Attack)
- **Stop asset inventory and misconfiguration detection** (IOMs)
- **Terminate sensor management capabilities** for EC2 instances
- **Disconnect EKS protection** if enabled
- **Remove ECR image scanning** if configured
- **Delete all EventBridge rules** for security event collection
- **Revoke CrowdStrike's access** to your AWS accounts

**After deletion, you will need to completely re-register your organization using CrowdStrike's default methods to restore security coverage.**

## Before You Begin

### Prerequisites
- Administrative access to the AWS management account or delegated administrator account
- Understanding that this is a **destructive operation** that cannot be easily undone
- Confirmation from security leadership that deregistration is intentional
- Plan for re-registration if security monitoring needs to be restored

### Impact Assessment
The CrowdStrike initialization stack creates numerous resources across your organization:

**Root Account Resources:**
- IAM roles and policies for CrowdStrike access
- Lambda functions for registration and orchestration
- S3 buckets for staging and deployment artifacts
- Organization-level CloudTrail (if created by the stack)
- EventBridge rules and targets for threat detection

**Member Account Resources (via StackSets):**
- Cloud Security Posture Management (CSPM) resources
- EventBridge rules for Indicators of Attack (IOA) detection
- SSM associations for Falcon sensor deployment
- EKS protection components (if enabled)
- ECR registry connections (if enabled)

## Deletion Process

### Step 1: Identify the Stack
1. Log in to the AWS Management Console in your organization's management account
2. Navigate to **CloudFormation** service
3. Locate the CrowdStrike initialization stack (typically named with prefix `cs-abi` or similar)
4. Note the stack name for deletion

### Step 2: Review Stack Dependencies
Before deletion, understand what will be removed:

```bash
# Use AWS CLI to describe the stack and its resources
aws cloudformation describe-stack-resources --stack-name <STACK_NAME>

# List all StackSets created by the stack
aws cloudformation list-stack-sets --status ACTIVE
```

### Step 3: Delete the CloudFormation Stack

**Option A: AWS Console**
1. In the CloudFormation console, select the CrowdStrike initialization stack
2. Click **Delete**
3. Confirm deletion when prompted
4. Monitor the deletion progress (this may take 15-30 minutes)

**Option B: AWS CLI**
```bash
# Delete the stack
aws cloudformation delete-stack --stack-name <STACK_NAME>

# Monitor deletion progress
aws cloudformation describe-stacks --stack-name <STACK_NAME>
```

### Step 4: Verify Complete Removal
The stack deletion process will automatically:
- Delete all nested stacks and StackSets
- Remove resources from all member accounts
- Clean up IAM roles and policies
- Delete S3 buckets (if they're empty)
- Remove EventBridge rules and targets

**Manual Cleanup (if needed):**
Some resources may require manual cleanup:

```bash
# Check for remaining CrowdStrike-related resources
aws iam list-roles --query 'Roles[?contains(RoleName, `crowdstrike`) || contains(RoleName, `cs-abi`)]'
aws s3 ls | grep -i crowdstrike
aws events list-rules --query 'Rules[?contains(Name, `cs-`) || contains(Name, `crowdstrike`)]'
```

## Post-Deletion Status

### Immediate Effects
Once the stack is deleted, your AWS Organization will be **completely disconnected** from CrowdStrike Falcon Cloud Security:

- ❌ **No security monitoring** across any AWS accounts
- ❌ **No threat detection** or incident alerts
- ❌ **No compliance monitoring** or misconfiguration alerts
- ❌ **No automated sensor deployment** capabilities
- ❌ **No container security** for EKS clusters
- ❌ **No image scanning** for ECR repositories

### CrowdStrike Console Impact
In the CrowdStrike Falcon console:
- Your AWS Organization will be removed from the Falcon Cloud Accounts registration page.

## Re-Registration Requirements

To restore CrowdStrike security monitoring after stack deletion, you **MUST** complete a full re-registration process using one of CrowdStrike's default Infrastructure as Code methods.

### Available Re-Registration Methods

Refer to the comprehensive benefits analysis in [`crowdstrike-aws-account-registration-benefits-summary.md`](./crowdstrike-aws-account-registration-benefits-summary.md) to choose the appropriate method:

#### Option 1: CloudFormation Re-deployment
**Best for:** Organizations seeking streamlined re-deployment with minimal technical overhead
- Use CrowdStrike's CloudFormation templates for automated organization-wide registration
- Provides wizard-driven process with built-in validation
- Automatically registers new AWS accounts added to the organization
- Minimal DevOps expertise required

#### Option 2: Terraform Re-deployment
**Best for:** Organizations with mature DevOps practices and advanced customization needs
- Deploy using CrowdStrike's Terraform modules
- Will not deploy any CloudFormation stacks, all resources under Terraform State Management
- Requires Terraform expertise and custom orchestration

For detailed information about the benefits and processes of CrowdStrike's default registration methods, see the comprehensive guide: [`crowdstrike-aws-account-registration-benefits-summary.md`](./crowdstrike-aws-account-registration-benefits-summary.md)
