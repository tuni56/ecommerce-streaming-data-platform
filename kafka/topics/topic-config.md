# Topic Configuration

This document describes topic-level configuration choices.

## page_views

- Partitions: high
- Replication factor: >= 2
- Retention: short (high volume)

## cart_events

- Partitions: medium
- Replication factor: >= 2
- Retention: medium

## purchase_events

- Partitions: low
- Replication factor: >= 3
- Retention: long (business critical)

## Rationale

Topic configuration reflects traffic patterns
and business criticality.
