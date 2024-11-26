 
#  Encapsulates the state of the service, such as readiness status.
class ServiceState:
   
    def __init__(self):
    # Readiness status (default: not ready)
        self.ready = False
    # Marks the service as ready.
    def mark_ready(self):
        self.ready = True
    # Marks the service as not ready.
    def mark_not_ready(self):
        self.ready = False
    # Checks if the service is ready.
    def is_ready(self):
        return self.ready
