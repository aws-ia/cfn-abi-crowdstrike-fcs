---
weight: 15
title: Cleanup instructions
description: Instructions to clean up the resources created by the ABI solution.
---

#### Remove Falcon Sensors deployed by SSM Distributor
1. Before deleting any stacks, first update the main template with the following change:
```
# Create SSM Distributor Associations
  AssociationStackSet:
    Type: 'AWS::CloudFormation::StackSet'
    Condition: CreateSSMAssociations
    Properties:
      StackSetName: CrowdStrike-Cloud-SSM-Associations-Stackset
      Description: Create SSM State Manager Association to automatically manage Falcon Sensor installation across SSM Managed Instances
      PermissionModel: SERVICE_MANAGED
      CallAs: !If [ IsDelegatedAdmin, 'DELEGATED_ADMIN', 'SELF' ]
      ManagedExecution:
        Active: true
      Parameters:
        - ParameterKey: DocumentVersion
          ParameterValue: !Ref DocumentVersion
        - ParameterKey: SecretsManagerSecretName
          ParameterValue: !Ref SecretsManagerSecretName
        - ParameterKey: SecretStorageMethod
          ParameterValue: 'SecretsManager'
        - ParameterKey: Action
          ParameterValue: 'Install'  <<Change to 'Uninstall'
```
2. Update the main stack, uploading the new version of the template.
3. This will update the 'action' on all State Manager Associations to 'Uninstall' and execute.
4. Wait until all associations have completed their Uninstall executions.


#### Remove Falcon Sensor deployed by EKS Protection
EKS Protection leverages the Falcon Operator, as such to remove any sensors deployed via this method please follow the uninstall steps for each cluster [here](https://github.com/CrowdStrike/falcon-operator/blob/main/docs/deployment/eks/README.md).


#### Cleanup instructions
The following must be completed before attempting to redeploy.

1. Delete CloudFormation Stack: 
    * Stack name: `template-crowdstrike-enable-integrations`
2. Empty and Delete S3 Bucket
    * S3 Bucket Name: aws-abi-${AWS::AccountId}-${AWS::Region}