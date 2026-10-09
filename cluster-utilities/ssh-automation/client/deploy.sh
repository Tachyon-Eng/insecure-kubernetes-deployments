#!/bin/bash


set -e










echo "Deleting existing pod to force restart..."
kubectl delete pod -l app=ssh-client --force --grace-period=0 -n erlang || true


echo "Deploying SSH client to Kubernetes..."
kubectl apply -f client-deployment.yaml -n erlang

echo "Deployment complete! Check the status with: kubectl get pods -l app=ssh-client"
