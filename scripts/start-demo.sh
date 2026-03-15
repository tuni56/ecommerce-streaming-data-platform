#!/bin/bash
set -e

CONTAINER="ecommerce-streaming"
KAFKA_HOME="/opt/kafka"
JAVA_HOME="/usr/lib/jvm/java-17-openjdk-amd64"
LOG="/var/log/kafka.log"

echo "🚀 Starting ecommerce streaming demo..."

# 1. Check container is running
if ! lxc list "$CONTAINER" --format csv | grep -q "RUNNING"; then
  echo "▶ Starting LXD container..."
  lxc start "$CONTAINER"
  sleep 3
fi

# 2. Check if Kafka is already running
if lxc exec "$CONTAINER" -- pgrep -f kafka.Kafka > /dev/null 2>&1; then
  echo "✅ Kafka already running — skipping start"
else
  echo "▶ Starting Kafka (KRaft)..."
  lxc exec "$CONTAINER" -- bash -c "
    export JAVA_HOME=$JAVA_HOME
    nohup $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/kraft/server.properties \
      > $LOG 2>&1 &
    echo \$! > /var/run/kafka.pid
  "
  sleep 5

  # Verify broker is up
  if ! lxc exec "$CONTAINER" -- pgrep -f kafka.Kafka > /dev/null 2>&1; then
    echo "❌ Kafka failed to start. Check logs: lxc exec $CONTAINER -- tail -20 $LOG"
    exit 1
  fi
  echo "✅ Kafka started"
fi

# 3. Create topics if they don't exist
echo "▶ Ensuring topics exist..."
lxc exec "$CONTAINER" -- bash -c "
  export JAVA_HOME=$JAVA_HOME
  for topic in page_views cart_events purchase_events; do
    $KAFKA_HOME/bin/kafka-topics.sh --bootstrap-server localhost:9092 \
      --create --if-not-exists --topic \$topic --partitions 3 --replication-factor 1 \
      2>/dev/null && echo \"  ✅ \$topic\" || echo \"  ✅ \$topic (already exists)\"
  done
"

echo ""
echo "✅ Demo environment ready!"
echo ""
echo "  Terminal 1 — Producer:"
echo "    lxc exec $CONTAINER -- /opt/ecommerce-venv/bin/python /tmp/producer.py"
echo ""
echo "  Terminal 2 — Consumer:"
echo "    lxc exec $CONTAINER -- $KAFKA_HOME/bin/kafka-console-consumer.sh \\"
echo "      --bootstrap-server localhost:9092 --topic page_views --from-beginning"
echo ""
echo "  Terminal 3 — Spark Streaming (aggregations every 10s):"
echo "    lxc exec $CONTAINER -- sh -c '"
echo "    export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64 &&"
echo "    export PYSPARK_PYTHON=/opt/ecommerce-venv/bin/python &&"
echo "    JARS=/opt/spark-jars/spark-sql-kafka-0-10_2.13-4.1.0.jar,/opt/spark-jars/kafka-clients-3.8.0.jar,/opt/spark-jars/spark-token-provider-kafka-0-10_2.13-4.1.0.jar,/opt/spark-jars/commons-pool2-2.12.0.jar &&"
echo "    /opt/ecommerce-venv/lib/python3.12/site-packages/pyspark/bin/spark-submit --jars \$JARS /tmp/spark_job.py'"
