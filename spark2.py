from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

import os

print("SPARK_HOME:", os.environ.get("SPARK_HOME"))
print("JAVA_HOME:", os.environ.get("JAVA_HOME"))
print("HADOOP_HOME:", os.environ.get("HADOOP_HOME"))
print("HADOOP_OPTS:", os.environ.get('HADOOP_OPTS'))

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkIntegration") \
    .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
    .config("spark.sql.adaptive.enabled", "false") \
    .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/test.myCollection2") \
    .getOrCreate()

spark.sparkContext.setLogLevel('ERROR')

# Read data from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "my_topic2") \
    .load()

# Select the value column and cast it to a string
kafka_df2 = kafka_df.selectExpr("CAST(value AS STRING)")

# Define schema for JSON data
innerSchema = StructType([
    StructField("_id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("exposure", StringType(), True),
    StructField("model", StringType(), True)
])
keys = ['_id', 'name', 'exposure', 'model']

# Parse JSON data
json_df = kafka_df2.select(from_json(col("value"), innerSchema).alias("data")).select("data.*")

# Write data to MongoDB
def write_to_mongo(batch_df, batch_id):
    batch_df.write \
            .format("mongo") \
            .mode("append") \
            .option("uri", "mongodb://127.0.0.1/test.myCollection2") \
            .save()

# # Write data to console for verification
queryConsole = json_df.writeStream \
               .outputMode("update") \
               .format("console") \
               .start()

# Write data to MongoDB
queryMongo = json_df.writeStream \
               .foreachBatch(write_to_mongo) \
               .outputMode("update") \
               .start()

# Await termination
queryConsole.awaitTermination()
queryMongo.awaitTermination()
