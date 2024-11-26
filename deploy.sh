#!/bin/bash

set -e  # Exit on any error
set -o pipefail  # Ensure pipeline errors are caught

# Define variables
NAMESPACE="namespace-watcher"
DOCKER_IMAGE="namespace_watcher:latest"
DEPLOYMENT_YAML="deployment.yaml"
HELM_CHART_PATH="helm"
TEMP_DEPLOYMENT_YAML="temp-deployment.yaml"
IMAGE_NAME=$DOCKER_IMAGE

# Function to check if the namespace exists, or create it if not
ensure_namespace_exists() {
  echo "Ensuring the namespace exists..."
  if ! kubectl get namespace $NAMESPACE &>/dev/null; then
    kubectl create namespace $NAMESPACE
    echo "Namespace '$NAMESPACE' created."
  else
    echo "Namespace '$NAMESPACE' already exists."
  fi
}

# Function to build the Docker image
build_docker_image() {
  echo "Building Docker image..."
  docker build -t $DOCKER_IMAGE .
}

# Function to deploy using raw YAML
deploy_with_yaml() {
  echo "Preparing to deploy using raw YAML..."
  
  echo "Substituting variables in deployment YAML..."
  export IMAGE_NAME=$DOCKER_IMAGE  # Export the variable for envsubst
  envsubst < $DEPLOYMENT_YAML > $TEMP_DEPLOYMENT_YAML
  
  echo "Temporary deployment file content:"
  cat $TEMP_DEPLOYMENT_YAML  # Debugging step to verify substitution

  echo "Ensuring the namespace exists..."
  ensure_namespace_exists

  if kubectl get deployment namespace-watcher -n $NAMESPACE &>/dev/null; then
    echo "Deployment 'namespace-watcher' already exists. Performing a rollout update..."
    kubectl apply -f $TEMP_DEPLOYMENT_YAML --namespace $NAMESPACE
    kubectl rollout restart deployment/namespace-watcher -n $NAMESPACE
  else
    echo "Deployment 'namespace-watcher' does not exist. Creating a new deployment..."
    kubectl apply -f $TEMP_DEPLOYMENT_YAML --namespace $NAMESPACE
  fi

  echo "Waiting for the deployment to be ready..."
  kubectl rollout status deployment/namespace-watcher -n $NAMESPACE

  # Clean up temporary file
  rm -f $TEMP_DEPLOYMENT_YAML
}

# Function to deploy using Helm chart
deploy_with_helm() {
  echo "Deploying using Helm chart..."
  ensure_namespace_exists
  echo "Installing or upgrading the Helm release..."
  helm upgrade --install namespace-watcher $HELM_CHART_PATH \
    --namespace $NAMESPACE 
}

# Function to verify the deployment
verify_deployment() {
  echo "Verifying deployment..."
  kubectl get pods -n $NAMESPACE

  echo "Fetching logs from the deployed pods..."
  for pod in $(kubectl get pods -n $NAMESPACE -o name); do
    kubectl logs -n $NAMESPACE $pod || echo "No logs available for $pod yet."
  done
}

# Main script execution
main() {
  echo "Select deployment method:"
  echo "1) Raw YAML"
  echo "2) Helm chart"
  read -p "Enter your choice [1/2]: " choice

  build_docker_image

  if [[ $choice == "1" ]]; then
    echo "You selected Raw YAML deployment."
    deploy_with_yaml
  elif [[ $choice == "2" ]]; then
    echo "You selected Helm chart deployment."
    deploy_with_helm
  else
    echo "Invalid choice. Exiting."
    exit 1
  fi

  verify_deployment
  echo "Namespace Watcher deployed successfully!"
}

# Run the main function
main "$@"
