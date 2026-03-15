import json
from kafka import KafkaConsumer

BOOTSTRAP_SERVERS = "10.34.23.19:9092"
TOPICS = ["page_views", "cart_events", "purchase_events"]

consumer = KafkaConsumer(
    *TOPICS,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="ecommerce-consumer-group"
)

ICONS = {
    "page_view": "👁 ",
    "cart_event": "🛒",
    "purchase":   "💰"
}

print(f"Consuming from {TOPICS} — Ctrl+C to stop\n")

try:
    for message in consumer:
        event = message.value
        icon = ICONS.get(event.get("event_type"), "📨")
        print(
            f"{icon} [{message.topic}] "
            f"user={event.get('user_id')} | "
            f"id={event.get('event_id', '')[:8]} | "
            f"ts={event.get('timestamp', '')[:19]}"
        )
except KeyboardInterrupt:
    print("\nConsumer stopped.")
finally:
    consumer.close()
