---
weight: 14
title: Troubleshooting
description: Troubleshooting.
---

#### General Troubleshooting
For troubleshooting issues with Falcon Cloud Security, submit a ticket on the [CrowdStrike support portal](https://supportportal.crowdstrike.com/).

For troubleshooting common ABI issues, refer to the [ABI Reference Guide](https://a.co/j72wxaw) and [Troubleshooting CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/troubleshooting.html).

#### SSM Distributor
1. Check the execution logs for the SSM State Manager Association. See [SSM Documentation](https://docs.aws.amazon.com/systems-manager/latest/userguide/state-manager-associations-history.html).

#### EKS Protection
1. Check the Lambda logs in CloudWatch Logs for ```crowdstrike-abi-eks-init-function``` and ```crowdstrike-abi-eks-events-function```.
2. Check the CodeBuild Execution logs for ```crowdstrike-eks-codebuild```.
3. Check the Falcon Operator logs on the cluster.  See [Operator Troubleshooting](https://github.com/CrowdStrike/falcon-operator/blob/main/docs/install_guide.md).

#### ECR Registry Connections
See falcon documentation for detailed troubleshooting information [here](https://falcon.crowdstrike.com/documentation/page/xfb81fc4/assess-image-from-registry#s2614b67).

**Next:** Choose [Feedback](/feedback/index.html).