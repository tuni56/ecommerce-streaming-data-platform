# Aggregation Strategy

This layer focuses on near-real-time aggregations.

## Examples

- Page views per minute
- Cart additions per product
- Purchase volume per hour

## Design Principles

- Window-based aggregations
- Tolerate late-arriving events
- Favor append-only outputs

Aggregations are designed to support dashboards
and operational visibility.
