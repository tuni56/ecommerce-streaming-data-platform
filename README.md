[![Kafka](https://img.shields.io/badge/Kafka-StreamingPipeline-orange?style=flat&logo=apachekafka)](https://kafka.apache.org/)
[![Grafana](https://img.shields.io/badge/Grafana-Monitoring-blue?style=flat&logo=grafana)](https://grafana.com/)
# Real-Time Ecommerce Streaming Data Platform

This repository documents the design and implementation of a real-time
data streaming platform for an ecommerce use case.

The project focuses on **data engineering fundamentals**:
event-driven architecture, Kafka-based ingestion, observability,
and infrastructure decisions that protect data producers at scale.

---

## Problem Statement

Ecommerce platforms generate continuous streams of events:

- page views
- cart interactions
- purchases

These events are:
- high volume
- bursty
- business critical

A key constraint guided this design:

**data producers must never break**, even as the platform evolves.

---

## Architectural Overview

All events enter the platform through a single, stable endpoint:

events.ecommerce-domain.com


Amazon Route 53 is used as a strategic routing layer to:
- decouple producers from backend infrastructure
- enable safe evolution of pipelines
- support failover and traffic spikes

Behind this entry point, Kafka handles durable ingestion and streaming.
<img width="1536" height="1024" alt="real-time_ecommerce_pipeline" src="https://github.com/user-attachments/assets/50df57e7-7446-4e81-886e-09f858a5469d" />

---

## Event Types

The platform processes three core event categories:

- **Page Views**
  - High volume, append-only
- **Cart Events**
  - Bursty traffic, user-driven
- **Purchase Events**
  - Low volume, business critical

Each event type is defined using explicit schemas
to enforce contracts between producers and consumers.

---

## Repository Structure

<img width="793" height="625" alt="Captura desde 2025-12-22 08-08-43" src="https://github.com/user-attachments/assets/6199c6c1-7036-48ef-a560-108ca0fa062a" />


---

## Kafka Design

- Producers publish events asynchronously
- Topics are partitioned based on access patterns
- Consumers are designed to be idempotent
- Consumer lag is treated as a first-class metric

Kafka configuration reflects traffic patterns
and business criticality rather than uniform defaults.

---

## Observability

Grafana dashboards track:
- ingestion rate
- consumer lag
- processing latency
- error rates

Observability is used not only for monitoring,
but to inform routing and scaling decisions.

---

## What This Project Demonstrates

This project is intentionally **not production-deployed**.

Its purpose is to demonstrate:
- data engineering thinking
- architectural trade-offs
- event-driven design
- Kafka fundamentals
- routing and resilience strategies

---

## Future Enhancements

- Traffic simulation for load testing
- Schema versioning and compatibility checks
- Infrastructure as Code (Terraform / CloudFormation)
- Stream processing with Kafka Streams or Flink

---

## Context

This project was built as a hands-on exercise to showcase
data engineering skills through realistic system design
and documented technical decisions.
