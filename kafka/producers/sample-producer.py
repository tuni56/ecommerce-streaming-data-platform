import json
import time
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="KAFKA_BOOTSTRAP_SERVERS",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

event = {
    "event_type": "page_view",
    "event_id": "uuid",
    "user_id": "user_123",
    "page_url": "/home",
    "timestamp": "2025-01-01T10:00:00Z"
}

producer.send("page_views", event)
producer.flush()

print("Event published")
