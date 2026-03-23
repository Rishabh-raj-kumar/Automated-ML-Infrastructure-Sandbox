# Local Cloud ML Sandbox: Zero-Cost AIOps Architecture

## Overview
This project provides a fully automated, local-first machine learning deployment environment. It simulates an enterprise-grade AWS cloud infrastructure on local hardware with zero associated cloud costs. By utilizing Infrastructure as Code (IaC) and container orchestration, it establishes a reliable pipeline for serving ML models via a REST API.

## System Architecture



The architecture consists of four primary layers:
1. **Infrastructure Provisioning:** Terraform handles the automated creation of the Kubernetes cluster.
2. **Container Orchestration:** Kind (Kubernetes in Docker) manages the worker nodes and pod lifecycles.
3. **Cloud Simulation:** LocalStack mimics AWS S3, acting as the object storage for machine learning artifacts (`model.pkl`).
4. **Application Layer:** A containerized FastAPI (Python) service retrieves the model from LocalStack into memory and serves predictions.

## Tech Stack
* **IaC:** Terraform
* **Orchestration:** Kubernetes (Kind)
* **Containerization:** Docker
* **Cloud Mocking:** LocalStack
* **Application:** Python 3.10, FastAPI, Boto3

## Prerequisites
Ensure the following CLI tools are installed on your local machine:
* Docker & Docker Compose
* Terraform
* kubectl
* kind
* AWS CLI

## Manual User Guide

### 1. Start the Cloud Storage Simulation
First, initialize LocalStack to mock the AWS environment.
```bash
docker-compose up -d
```
Verify the container is running and create the mock S3 bucket:
```bash
aws --endpoint-url=http://localhost:4566 s3 mb s3://ml-models-bucket
```
Generate and upload a dummy ML model to the local bucket:
```bash
python -c "import pickle; pickle.dump({'model_name': 'AIOps Predictive Engine', 'version': '1.0.0', 'status': 'Active'}, open('model.pkl', 'wb'))"
aws --endpoint-url=http://localhost:4566 s3 cp model.pkl s3://ml-models-bucket/model.pkl
```

### 2. Provision Infrastructure
Navigate to the terraform directory to create the Kubernetes cluster.
```bash
cd terraform
terraform init
terraform apply -auto-approve
cd ..
```

### 3. Build and Load the Application
Build the Docker image for the Python API and load it directly into the Kind cluster registry to avoid remote pulling.
```bash
cd app
docker build -t local-ml-api:v2 .
kind load docker-image local-ml-api:v2 --name ml-sandbox-cluster
cd ..
```

### 4. Deploy to Kubernetes
Apply the deployment and service manifests to start the pods and configure networking.
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 5. Access the API
Forward the Kubernetes service port to your local machine:
```bash
kubectl port-forward service/ml-app-service 8000:80
```
Test the endpoint via curl or your browser:
```bash
curl "http://localhost:8000/predict?input_data=server_logs_001"
```
**Expected Output:**
```json
{
  "status": "success",
  "input_received": "server_logs_001",
  "active_model": {"model_name": "AIOps Predictive Engine", "version": "1.0.0", "status": "Active"},
  "prediction": "AIOps analysis complete for: server_logs_001"
}
```

## Teardown and Cleanup
To destroy the resources and free up system memory, run the following commands:
```bash
# Destroy Kubernetes cluster
cd terraform
terraform destroy -auto-approve
cd ..

# Stop LocalStack
docker-compose down

