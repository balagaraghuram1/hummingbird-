"""Prometheus metrics for monitoring.

Defines application-specific metrics for monitoring
API performance and AI model usage.
"""

from __future__ import annotations

from prometheus_client import Counter, Histogram, Info

APP_INFO = Info("hummingbird", "Hummingbird Medical AI application info")

REQUEST_COUNT = Counter(
    "hummingbird_requests_total",
    "Total API requests",
    ["method", "endpoint", "status"],
)

REQUEST_LATENCY = Histogram(
    "hummingbird_request_latency_seconds",
    "API request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

AI_REQUEST_COUNT = Counter(
    "hummingbird_ai_requests_total",
    "Total AI model requests",
    ["provider", "model", "status"],
)

AI_REQUEST_LATENCY = Histogram(
    "hummingbird_ai_request_latency_seconds",
    "AI model request latency",
    ["provider", "model"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
)

CACHE_HITS = Counter(
    "hummingbird_cache_hits_total",
    "Total cache hits",
    ["cache_type"],
)

CACHE_MISSES = Counter(
    "hummingbird_cache_misses_total",
    "Total cache misses",
    ["cache_type"],
)

DIAGNOSIS_COUNT = Counter(
    "hummingbird_diagnoses_total",
    "Total diagnosis requests processed",
)

TREATMENT_COUNT = Counter(
    "hummingbird_treatments_total",
    "Total treatment plans generated",
)

LAB_ANALYSIS_COUNT = Counter(
    "hummingbird_lab_analyses_total",
    "Total lab analyses performed",
)
