from prometheus_client import Counter, Histogram, CollectorRegistry
import time

class MetricsTracker:
    def __init__(self):
        self.registry = CollectorRegistry()
        
        # Create metrics
        self.inference_time = Histogram(
            'model_inference_time_seconds',
            'Time spent processing each request',
            registry=self.registry
        )
        self.requests_total = Counter(
            'model_requests_total',
            'Total number of requests processed',
            registry=self.registry
        )
        self.successful_requests = Counter(
            'model_successful_requests',
            'Number of successful requests',
            registry=self.registry
        )
        self.failed_requests = Counter(
            'model_failed_requests',
            'Number of failed requests',
            registry=self.registry
        )

    def track_request(self, inference_time: float, success: bool):
        self.inference_time.observe(inference_time)
        self.requests_total.inc()
        if success:
            self.successful_requests.inc()
        else:
            self.failed_requests.inc()