# Stream Processing Notes

This layer is responsible for real-time transformations and aggregations.

## Responsibilities

- Validate incoming events
- Enrich events with derived fields
- Produce aggregated metrics

## Design Principles

- Stateless processing where possible
- Idempotent transformations
- Late event tolerance for page views

Processing logic is intentionally abstracted to allow
multiple implementations (Kafka Streams, Flink, Spark Structured Streaming).
