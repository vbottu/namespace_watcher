from threading import Thread
from service.health_check import start_health_server
from service.namespace_watcher import NamespaceWatcher
from prometheus_client import start_http_server
from service.logger_config import get_logger
from service.service_state import ServiceState
from datetime import datetime, timezone
import time

logger = get_logger("NamespaceWatcher")
service_start_time = datetime.now(timezone.utc)


def main():
    try:
        # Initialize the shared service state
        service_state = ServiceState()

        # Start Prometheus metrics server
        start_http_server(8000)
        logger.info("Prometheus metrics server running on port 8000")
        
         # Start the health check server in a separate thread
        health_thread = Thread(target=start_health_server,args=(service_state,), daemon=True)
        health_thread.start()

        logger.info("Initializing the NamespaceWatcher service...")
        service_state.mark_not_ready()  # Mark as not ready during initialization

        # Initialize and start the namespace watcher
        watcher = NamespaceWatcher(service_start_time)
        service_state.mark_ready()
        time.sleep(5)
        watcher.watch_namespaces()
        

    except Exception as e:
        logger.error(f"Fatal error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
