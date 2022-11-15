import json
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import window, col
from pyspark.sql.types import StringType, IntegerType, TimestampType, StructType, StructField

from waimea.config import API_HOST, API_PORT

def process_batch(out_df, batch_id):
        out_df.persist()

        for i in out_df.collect():
            if i["avg(wave_height)"]>25:
                serialized_data = json.dumps(int(round(i["avg(wave_height)"])))
                requests.post('http://api:8080/alert', data=serialized_data)

        out_df.unpersist()

def main():
    # TODO:
    #  1) Using PySpark, analyze the streaming log files to detect whether, over the past 30 minutes,
    #       the mean wave height has been > 25'
    #  2) When a proper big wave swell is detected, send an alert to to the http://API_HOST:API_PORT/alert endpoint

    spark = SparkSession.builder.appName("detector").getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    schema = StructType([
        StructField("input_timestamp", TimestampType(), True),
        StructField("wave_height", StringType(), True)
    ])

    # Used .csv() instead of .load() method and .log file format to avoid expected Parquet error
    # TODO: consider using .filter here instead of conditional within foreachBatch
    wave_values = spark.readStream\
        .schema(schema)\
        .option("delimiter", ",")\
        .option("multiline", "true")\
        .csv("./logs")\
        .withColumn("wave_height", col("wave_height").astype(IntegerType()))\
        .withWatermark("input_timestamp", "30 minutes")\
        .groupBy(window("input_timestamp","30 minutes","1 minute"))\
        .avg("wave_height")

    wave_values.createOrReplaceTempView("streaming_wave_values")
                
    out_df = spark.sql("select * from streaming_wave_values")

    # TODO: verify that append ensures only new records trigger the foreachBatch condition
    out_df.writeStream\
        .foreachBatch(process_batch)\
        .queryName("conditional_check")\
        .outputMode("append")\
        .start()\
        .awaitTermination()
