#!/bin/bash
echo "Registry is $REGISTRY"
if [ $REGISTRY == "ecr" ]; then

    echo "Getting ECR login..."
    aws ecr get-login-password --region $IMAGE_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$IMAGE_REGION.amazonaws.com
    ecr_uri="$ACCOUNT_ID.dkr.ecr.$IMAGE_REGION.amazonaws.com/crowdstrike"

    echo "Pushing Node Sensor image..."
    
    node_sensor_repo="crowdstrike/falcon-sensor"
    curl https://raw.githubusercontent.com/CrowdStrike/falcon-scripts/main/bash/containers/falcon-container-sensor-pull/falcon-container-sensor-pull.sh | bash -s -- -u $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -t 'falcon-sensor' -c $ecr_uri
    echo "export NODE_SENSOR_URI=$ACCOUNT_ID.dkr.ecr.$IMAGE_REGION.amazonaws.com/$node_sensor_repo" >> /root/.bashrc
    node_sensor_tag=$(aws ecr list-images --repository-name $node_sensor_repo --query 'imageIds[*].imageTag' --output text)
    echo "export NODE_SENSOR_TAG=$node_sensor_tag" >> /root/.bashrc

    echo "Pushing KPA image..."
    
    kpa_repo="crowdstrike/kpagent"
    curl https://raw.githubusercontent.com/CrowdStrike/falcon-scripts/main/bash/containers/falcon-container-sensor-pull/falcon-container-sensor-pull.sh | bash -s -- -u $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -t 'kpagent' -c $ecr_uri
    echo "export KPA_URI=$ACCOUNT_ID.dkr.ecr.$IMAGE_REGION.amazonaws.com/$kpa_repo" >> /root/.bashrc
    kpa_tag=$(aws ecr list-images --repository-name $kpa_repo --query 'imageIds[*].imageTag' --output text)
    echo "export KPA_TAG=$kpa_tag" >> /root/.bashrc

elif [ $REGISTRY == "crowdstrike" ]; then

    echo "Getting KPA image..."

    curl https://raw.githubusercontent.com/CrowdStrike/falcon-scripts/main/bash/containers/falcon-container-sensor-pull/falcon-container-sensor-pull.sh | bash -s -- -u $FALCON_CLIENT_ID -s $FALCON_CLIENT_SECRET -t 'kpagent'
    echo "export KPA_URI=registry.crowdstrike.com/kubernetes_protection/kpagent" >> /root/.bashrc
    kpa_tag=$(docker images registry.crowdstrike.com/kubernetes_protection/kpagent --format "{{.Tag}}")
    echo "export KPA_TAG=$kpa_tag" >> /root/.bashrc
    
else
    echo "Missing env variable REGISTRY"
fi