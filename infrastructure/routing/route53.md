
# Amazon Route 53 in the Data Platform

Amazon Route 53 is used as a strategic routing layer,
not just as a DNS service.

## Core Responsibilities

- Provide a stable ingestion endpoint
- Decouple producers from backend infrastructure
- Support traffic-based routing decisions

## Ingestion Domain

events.ecommerce-domain.com


Producers publish events to this domain and are unaware
of backend services, clusters, or regions.

## Why DNS-Level Routing

- No client redeployment required
- Routing changes are transparent to producers
- Infrastructure can evolve independently
