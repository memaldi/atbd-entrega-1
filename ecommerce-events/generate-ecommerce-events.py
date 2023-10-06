#!/usr/bin/env python
# coding: utf-8

import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as f
from datetime import datetime
from kafka import KafkaProducer

spark = SparkSession.builder.getOrCreate()

# Change this to point to the folder where all the data remains
events = spark.read.csv("../2019-Dec.csv", header=True)

first_event = datetime.strptime(events.select("event_time").sort("event_time").first().event_time, "%Y-%m-%d %H:%M:%S %Z")

substract_date = f.udf(lambda event_time: (datetime.strptime(event_time, "%Y-%m-%d %H:%M:%S %Z") - first_event).seconds)

events_with_delta = events.withColumn("delta", substract_date(events.event_time))

current_delta = 0

# Switch to real Kafka port
producer = KafkaProducer(bootstrap_servers='localhost:9020')

while True:
    print("Current delta: {current_delta}".format(current_delta=current_delta))
    current_events = events_with_delta.filter(events_with_delta.delta == current_delta)
    current_timestamp = datetime.now()
    for event in current_events.collect():
        json_event = { "event_time": current_timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"), 
                      "event_type": event.event_type, 
                      "product_id": event.product_id, 
                      "category_id": event.category_id, 
                      "brand": event.brand,
                      "price": event.price,
                      "user_id": event.user_id,
                      "user_session": event.user_session}

        producer.send('ecommerce-events', json_event)
    time.sleep(1)
    current_delta += 1
