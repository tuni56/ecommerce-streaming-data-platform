# Failover Strategy

The platform is designed to tolerate partial failures.

## Failure Scenarios

- Kafka broker degradation
- Processing slowdown
- Regional connectivity issues

## Route 53 Capabilities Used

- Health checks
- Failover routing
- Latency-based routing

## Outcome

Producers continue sending events
even when backend components fail or degrade.
