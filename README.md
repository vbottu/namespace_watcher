# Namespace Watcher Service

## Overview
The Namespace Watcher Service monitors Kubernetes for namespace creation events and creates a pod in each new namespace.

## Features
- Watches namespace creation events in real-time.
- Creates a pod in each new namespace with retry logic.
- Exposes Prometheus metrics for monitoring.

## Running Locally
1. Build the Docker image:
   ```bash
   docker build -t namespace-watcher .
   ```
2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 namespace-watcher
   ```

## Deployment on Kubernetes
1. Apply the Deployment YAML:
   ```bash
   kubectl apply -f deployment.yaml
   ```
2. Verify pod creation:
   ```bash
   kubectl get pods
   ```

## Observability
Prometheus metrics are exposed at `http://<pod-ip>:8000.
