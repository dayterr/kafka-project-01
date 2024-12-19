import time

from confluent_kafka import Producer

from utils import delivery_report, Message, MessageSerializer, TOPIC_NAME

conf = {
    "bootstrap.servers": "localhost:9092",
    "acks": "all",
    "retries": 5, 
} 

producer = Producer(conf)
message = Message('some header', 'some message')
serializer = MessageSerializer()

while True:
    producer.produce(topic=TOPIC_NAME, value=serializer(message), callback=delivery_report)
    producer.flush()
    time.sleep(5)
