---
weight: 99
title: Cleanup instructions
description: Instructions to clean up the resources created by the ABI solution.
---
## Cleanup instructions

1. Delete CloudFormation Stack: 
    * Stack name: `template-crowdstrike-enable-integrations`
2. Empty and Delete S3 Bucket
    * S3 Bucket Name: aws-abi-${AWS::AccountId}-${AWS::Region}
