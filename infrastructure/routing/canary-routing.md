# Canary Routing Strategy

Canary routing is used to safely validate changes
in the ingestion and processing layers.

## Use Cases

- New Kafka cluster
- Schema evolution
- Updated processing logic

## Strategy

- 90% of traffic → stable pipeline
- 10% of traffic → canary pipeline

Routing weights are adjusted gradually
based on system health and observability signals.

## Rollback

If error rate or consumer lag increases,
traffic is immediately routed back to the stable pipeline.
