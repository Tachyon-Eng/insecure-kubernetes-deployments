#!/bin/bash

# Exit on error
set -e

## Build the Docker image
#echo "Building SSH client Docker image..."
#docker build -t confusedcrib/ssh-client:latest -f client.Dockerfile .
#
## Push the Docker image
#echo "Pushing SSH client Docker image..."
#docker push confusedcrib/ssh-client:latest

# Delete existing pod to force restart
echo "Deleting existing pod to force restart..."
kubectl delete pod -l app=ssh-client --force --grace-period=0 -n erlang || true

# Deploy to Kubernetes
echo "Deploying SSH client to Kubernetes..."
kubectl apply -f client-deployment.yaml -n erlang

echo "Deployment complete! Check the status with: kubectl get pods -l app=ssh-client"
