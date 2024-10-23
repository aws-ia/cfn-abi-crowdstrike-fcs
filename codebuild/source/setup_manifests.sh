#!/bin/bash
CID_LOWER=$(echo $CID | cut -d '-' -f 1 | tr '[:upper:]' '[:lower:]')
sed -i "s~FALCON_CLIENT_ID~$FALCON_CLIENT_ID~" kpa_config.value
sed -i "s~FALCON_CLIENT_SECRET~$FALCON_CLIENT_SECRET~" kpa_config.value
sed -i "s~KPA_URI~$KPA_URI~" kpa_config.value
sed -i "s~KPA_TAG~$KPA_TAG~" kpa_config.value
sed -i "s~CLUSTER_ARN~$CLUSTER_ARN~" kpa_config.value
sed -i "s~CROWDSTRIKE_CLOUD~$CROWDSTRIKE_CLOUD~" kpa_config.value
sed -i "s~CID_LOWER~$CID_LOWER~" kpa_config.value
sed -i "s~DOCKER_API_TOKEN~$DOCKER_API_TOKEN~" kpa_config.value

if [ $REGISTRY == "ecr" ]; then
    sed -i "s~NODE_SENSOR_URI~$NODE_SENSOR_URI~" node_sensor_ecr.yaml
    sed -i "s~NODE_SENSOR_TAG~$NODE_SENSOR_TAG~" node_sensor_ecr.yaml
    sed -i "s~BACKEND~$BACKEND~" node_sensor_ecr.yaml
    sed -i "s~CID~$CID~" node_sensor_ecr.yaml
elif [ $REGISTRY == "crowdstrike" ]; then
    sed -i "s~FALCON_CLIENT_ID~$FALCON_CLIENT_ID~" node_sensor.yaml
    sed -i "s~FALCON_CLIENT_SECRET~$FALCON_CLIENT_SECRET~" node_sensor.yaml
    sed -i "s~BACKEND~$BACKEND~" node_sensor.yaml
fi

sed -i "s~REGISTRY~$REGISTRY~" sidecar_sensor.yaml
sed -i "s~REGISTRY~$REGISTRY~" falcon_admission.yaml
sed -i "s~FALCON_CLIENT_ID~$FALCON_CLIENT_ID~" sidecar_sensor.yaml
sed -i "s~FALCON_CLIENT_SECRET~$FALCON_CLIENT_SECRET~" sidecar_sensor.yaml
sed -i "s~FALCON_CLIENT_ID~$FALCON_CLIENT_ID~" falcon_admission.yaml
sed -i "s~FALCON_CLIENT_SECRET~$FALCON_CLIENT_SECRET~" falcon_admission.yaml
