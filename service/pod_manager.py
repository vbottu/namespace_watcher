from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from kubernetes import client
from service.utils import simulate_transient_failure
from service.logger_config import get_logger

# Set up a logger for pod management
logger = get_logger("PodManager")

# Manages pod creation in Kubernetes namespaces, including retry logic for transient failures.
class PodManager:

    @staticmethod
    @retry(
        stop=stop_after_attempt(3),  # Stop retrying after 3 attempts
        wait=wait_exponential(multiplier=1, max=10),  # Exponential backoff with a max delay of 10 seconds
        retry=retry_if_exception_type(client.exceptions.ApiException),  # Retry only on Kubernetes API errors
        reraise=True,  # Raise the exception if retries are exhausted
    )
    # Creates a pod in the specified namespace with retry logic for handling transient failures.
    def create_pod(namespace: str):
        
        # Initialize the CoreV1 API client for interacting with Kubernetes resources
        core_api = client.CoreV1Api()

        # Define the pod manifest (YAML structure) for the pod to be created
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": "echo-namespace-name"},  # Pod name
            "spec": {
                "containers": [
                    {
                        "name": "echo-namespace-name",  # Container name
                        "image": "busybox",  # Lightweight image for simple tasks
                        "command": ["/bin/sh", "-c", f"echo Namespace: {namespace} && sleep 5 && exit 0"],
                    }
                ],
                "restartPolicy": "Never",  # Ensure the pod does not restart after completing its task
            },
        }

        # Simulate transient failures for testing the retry mechanism
        simulate_transient_failure(namespace)

        try:
            # Attempt to create the pod in the specified namespace
            core_api.create_namespaced_pod(namespace=namespace, body=pod_manifest)
            logger.info(f"Pod successfully created in namespace: {namespace}")
        except client.exceptions.ApiException as e:
            if e.status == 409:
                # Handle the case where the pod already exists
                logger.warning(f"Pod already exists in namespace: {namespace}")
            else:
                # Log any other errors and re-raise the exception for retry
                logger.error(f"Error creating pod in namespace {namespace}: {e}")
                raise
