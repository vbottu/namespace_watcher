from prometheus_client import Counter
from service.logger_config import get_logger
logger=get_logger("metrics")
# Metrics for monitoring namespace creation events and retries
namespace_created_total = Counter(
    "namespace_created_total", "Number of namespaces detected and processed"
)
namespace_pod_creation_retries_total = Counter(
    "namespace_pod_creation_retries", "Total retry attempts for pod creation"
)
