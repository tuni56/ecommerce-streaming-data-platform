# Kafka Consumers

Consumers process events published to Kafka topics.

## Responsibilities

- Validate incoming events
- Apply lightweight transformations
- Forward events to downstream processing layers

## Design Notes

- Consumers are designed to be idempotent
- Offset management is handled explicitly
- Consumer lag is a key observability signal
