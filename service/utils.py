from kubernetes import client
from service.logger_config import get_logger
from service.metrics import namespace_pod_creation_retries_total

# A dictionary to track the number of simulated failures for each namespace
failure_simulation_counter = {}
logger = get_logger("utils")

# Simulates transient failures for testing retry mechanisms.
def simulate_transient_failure(namespace: str):
    
    # Initialize the failure counter for the namespace if it doesn't exist
    if namespace not in failure_simulation_counter:
        failure_simulation_counter[namespace] = 0

    # Increment the counter for the namespace
    failure_simulation_counter[namespace] += 1
    attempt = failure_simulation_counter[namespace]

    # Simulate failure for the first two attempts
    if attempt < 3:
        logger.warning(
            f"Simulating transient failure for namespace '{namespace}', attempt {attempt}"
        )
        namespace_pod_creation_retries_total.inc()
        raise client.exceptions.ApiException(   
            status=500, reason="Simulated transient error"
        )
    else:
        logger.info(f"Namespace '{namespace}' passed simulation on attempt {attempt}")

