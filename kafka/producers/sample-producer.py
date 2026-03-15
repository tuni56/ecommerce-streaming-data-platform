import json
import time
import uuid
import random
from datetime import datetime, timezone
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = "10.34.23.19:9092"

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

USERS = [f"user_{i}" for i in range(1, 6)]
PAGES = ["/home", "/products", "/cart", "/checkout"]
PRODUCTS = [f"prod_{i}" for i in range(100, 106)]

def page_view():
    return {
        "event_type": "page_view",
        "event_id": str(uuid.uuid4()),
        "user_id": random.choice(USERS),
        "page_url": random.choice(PAGES),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def cart_event():
    return {
        "event_type": "cart_event",
        "event_id": str(uuid.uuid4()),
        "user_id": random.choice(USERS),
        "product_id": random.choice(PRODUCTS),
        "action": random.choice(["add", "remove"]),
        "quantity": random.randint(1, 3),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

def purchase_event():
    return {
        "event_type": "purchase",
        "event_id": str(uuid.uuid4()),
        "user_id": random.choice(USERS),
        "order_id": str(uuid.uuid4()),
        "total_amount": round(random.uniform(10.0, 500.0), 2),
        "currency": "USD",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

EVENTS = [
    ("page_views", page_view, 5),
    ("cart_events", cart_event, 3),
    ("purchase_events", purchase_event, 1),
]

print(f"Producing events to {BOOTSTRAP_SERVERS} — Ctrl+C to stop\n")

try:
    while True:
        for topic, builder, weight in EVENTS:
            for _ in range(weight):
                event = builder()
                producer.send(topic, event)
                print(f"[{topic}] {event['event_type']} | user={event['user_id']} | id={event['event_id'][:8]}")
        producer.flush()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProducer stopped.")
finally:
    producer.close()
