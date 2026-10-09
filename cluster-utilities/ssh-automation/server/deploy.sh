#!/bin/bash








kubectl apply -f ssh-server-deployment.yaml -n erlang

echo "SSH server deployed successfully in the erlang namespace!"
echo "You can connect to the server using:"
echo "kubectl port-forward service/ssh-server 2222:22 -n erlang"
