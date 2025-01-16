#!/bin/bash

role_arn=arn:aws:iam::${ACCOUNT_ID}:role/${SWITCH_ROLE}
OUT=$(aws sts assume-role --role-arn $role_arn --role-session-name crowdstrike-eks-codebuild);\
export AWS_ACCESS_KEY_ID=$(echo $OUT | jq -r '.Credentials''.AccessKeyId');\
export AWS_SECRET_ACCESS_KEY=$(echo $OUT | jq -r '.Credentials''.SecretAccessKey');\
export AWS_SESSION_TOKEN=$(echo $OUT | jq -r '.Credentials''.SessionToken');

echo "Creating kubeconfig for $CLUSTER"
aws eks update-kubeconfig --region $AWS_REGION --name $CLUSTER

export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""

pods=$(kubectl get pods -A)
case "$pods" in 
    *kpagent*) 
        echo "Protection Agent already installed on cluster: $CLUSTER" 
        ;;
    *)
        echo "Installing Protection Agent..."
        helm upgrade --install -f kpa_config.value --create-namespace -n falcon-kubernetes-protection kpagent crowdstrike/cs-k8s-protection-agent
        ;;
esac
case "$pods" in 
    *falcon-operator*) 
        echo "Operator already installed on cluster: $CLUSTER" 
        ;;
    *)
        echo "Installing Operator..."
        if [ $REGISTRY == "ecr" ]; then
            eksctl utils associate-iam-oidc-provider --region $AWS_REGION --cluster $CLUSTER --approve
            kubectl apply -f https://github.com/CrowdStrike/falcon-operator/releases/latest/download/falcon-operator.yaml
            kubectl set env -n falcon-operator deployment/falcon-operator-controller-manager AWS_REGION=$IMAGE_REGION
        else
            kubectl apply -f https://github.com/CrowdStrike/falcon-operator/releases/latest/download/falcon-operator.yaml
        fi
        ;;
esac
case "$pods" in 
    *falcon-node-sensor*) 
        echo "Sensor already installed on cluster: $CLUSTER" 
        ;;
    *)
        
        echo "Installing node sensor..."
        if [ $REGISTRY == "ecr" ]; then 
            kubectl create -f node_sensor_ecr.yaml
        else 
            kubectl create -f node_sensor.yaml
        fi
        ;;
esac
if [ $ENABLE_KAC == "true" ]; then
    case "$pods" in 
        *falcon-admission*) 
            echo "Admission Controller already installed on cluster: $CLUSTER" 
            ;;
        *)
            echo "Installing Admission Controller..."
            kubectl create -f falcon_admission.yaml
            ;;
    esac
fi
