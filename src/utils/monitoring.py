from prometheus_client import Counter, Histogram


REQUEST_COUNT = Counter("hummingbird_requests_total", "Total API requests")
REQUEST_LATENCY = Histogram("hummingbird_request_latency_seconds", "API latency")

