from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, count
from pyspark.sql.types import StructType, StringType, DoubleType, IntegerType

BOOTSTRAP_SERVERS = "10.34.23.19:9092"
TOPICS = "page_views,cart_events,purchase_events"

spark = (
    SparkSession.builder
    .appName("EcommerceStreamingJob")
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0")
    .config("spark.sql.shuffle.partitions", "2")
    .getOrCreate()
)
spark.sparkContext.setLogLevel("WARN")

# Common schema fields
base_schema = StructType() \
    .add("event_type", StringType()) \
    .add("event_id", StringType()) \
    .add("user_id", StringType()) \
    .add("timestamp", StringType())

# Read from all topics
raw = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS)
    .option("subscribe", TOPICS)
    .option("startingOffsets", "latest")
    .load()
)

# Parse JSON payload
events = raw.select(
    col("topic"),
    from_json(col("value").cast("string"), base_schema).alias("data"),
    col("timestamp").alias("kafka_ts")
).select("topic", "data.*", "kafka_ts")

# Aggregate: event count per type per 10-second window
agg = (
    events
    .withWatermark("kafka_ts", "10 seconds")
    .groupBy(
        window("kafka_ts", "10 seconds"),
        col("event_type")
    )
    .agg(count("*").alias("event_count"))
    .select(
        col("window.start").alias("window_start"),
        col("window.end").alias("window_end"),
        col("event_type"),
        col("event_count")
    )
)

# Print to console
query = (
    agg.writeStream
    .outputMode("update")
    .format("console")
    .option("truncate", False)
    .trigger(processingTime="5 seconds")
    .start()
)

print("Spark Streaming job started — aggregating events every 10s. Ctrl+C to stop.")
query.awaitTermination()
