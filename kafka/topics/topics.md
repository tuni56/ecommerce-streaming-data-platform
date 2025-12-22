# Kafka Topics

This document defines the main Kafka topics used by the platform.

## Topics

- `page_views`
  - High-volume, append-only events
  - Partitioned by user_id

- `cart_events`
  - Bursty traffic
  - Partitioned by user_id

- `purchase_events`
  - Business-critical events
  - Partitioned by order_id

## Design Considerations

- Topics are designed around access patterns
- Partitioning keys are chosen to balance load and ordering
- Retention policies differ by event criticality
