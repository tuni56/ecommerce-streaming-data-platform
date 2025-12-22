import json
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    "page_views",
    bootstrap_servers="KAFKA_BOOTSTRAP_SERVERS",
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=False
)

for message in consumer:
    event = message.value
    print(f"Received event: {event}")
