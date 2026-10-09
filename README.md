# Kubernetes Application Suite

This repository contains a small collection of services and the infrastructure used to run them together. It is intended for local development and disposable Kubernetes environments.

## Components

- **Operations Console**: Flask application on port 8080
- **Cat Gallery**: Spring Boot application on port 8080
- **Inventory Web**: Node.js application on port 3000
- **Game API**: FastAPI application on port 8000
- **Code Review**: Flask application on port 5000
- **Diagnostics Runner**: containerized system diagnostics tools

## Run with Docker Compose

Build and start the services:

```bash
docker compose up --build
```

The Operations Console is available at `http://localhost:8080`, Cat Gallery at `http://localhost:8081`, Inventory Web at `http://localhost:3000`, and Game API at `http://localhost:8000`.

## Deploy to Kubernetes

The Terraform configuration creates an EKS cluster, and the Helm chart installs the application suite.

1. Install Terraform, Helm, the AWS CLI, and `kubectl`.
2. Create the cluster:

   ```bash
   cd terraform
   terraform init
   terraform apply
   aws eks --region "$(terraform output -raw region)" update-kubeconfig \
     --name "$(terraform output -raw cluster_name)"
   ```

3. Install the chart:

   ```bash
   cd ../application-suite
   helm install application-suite . --create-namespace --namespace operations-console
   ```

4. Remove the cluster when finished:

   ```bash
   cd ../terraform
   terraform destroy
   ```

Use the values in `application-suite/values.yaml` to configure images, namespaces, replica counts, and service ports.
