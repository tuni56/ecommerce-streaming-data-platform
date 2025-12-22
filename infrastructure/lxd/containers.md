# LXD Container Strategy

The platform is deployed using LXD containers.

## Containers

### data-eng-main
- Kafka
- Producers
- Consumers
- Aggregations

### data-eng-db
- Downstream persistence
- Aggregated metrics storage

### data-eng-monitor
- Grafana dashboards
- Monitoring and alerts

## Rationale

LXD provides:
- lightweight isolation
- VM-like networking
- reproducible local environments

This setup mirrors real-world separation of concerns
without requiring cloud deployment.
