from kubernetes import client, config, watch
from service.pod_manager import PodManager
from service.metrics import namespace_created_total
from service.logger_config import get_logger
import os

# Set up a logger for the namespace watcher
logger = get_logger("NamespaceWatcher")

#  Watches Kubernetes namespace events and takes action on newly created namespaces.
class NamespaceWatcher:
    
    #  Initialize the NamespaceWatcher with the service start time and Kubernetes client.
    def __init__(self, service_start_time):
        self.service_start_time = service_start_time
        self.v1 = self._initialize_kubernetes_client()
    # Setup kubernetes client for interacting with the cluster
    def _initialize_kubernetes_client(self):
        try:
            if "KUBERNETES_SERVICE_HOST" in os.environ:
            # Use in-cluster configuration
                config.load_incluster_config()
            else:
            # Use local kubeconfig
                config.load_kube_config()
            return client.CoreV1Api()
        except Exception as e:
            raise Exception(f"Failed to initialize Kubernetes client: {e}")
    # Start watching for namespace creation events and process them using the events from kubernetes watch api
    def watch_namespaces(self):
        logger.info(f"Namespace watcher started at {self.service_start_time.isoformat()}")
        watcher = watch.Watch()

        # Start streaming namespace events
        for event in watcher.stream(self.v1.list_namespace):
            # Process only new namespaces (event type: "ADDED")
            if event["type"] == "ADDED":
                namespace = event["object"].metadata.name
                creation_time = event["object"].metadata.creation_timestamp

                # Only act on namespaces created after the service started
                if creation_time and creation_time > self.service_start_time:
                    logger.info(f"New namespace detected: {namespace}, created at {creation_time}")

                    # Increment Prometheus counter for tracking namespace events
                    namespace_created_total.inc()

                    # Create a pod in the new namespace, with retry logic
                    try:
                        PodManager.create_pod(namespace)
                    except Exception as e:
                        # Log failures after retrying
                        logger.error(f"Failed to create pod in namespace {namespace} after retries: {e}")
                else:
                    # Skip namespaces that existed before the service started
                    logger.info(f"Ignoring pre-existing namespace: {namespace}, created at {creation_time}")
