import logging
from random import randint
import time

from confluent_kafka import Producer

from utils import delivery_report, Message, MessageSerializer, TOPIC_NAME

logger = logging.getLogger(__name__)

conf = {
    "bootstrap.servers": "127.0.0.1:9094,127.0.0.1:9095,127.0.0.1:9096",
    "acks": "all",
    "retries": 5, 
} 

logger.info('producer started')

producer = Producer(conf)
serializer = MessageSerializer()

while True:
    message = Message('some header', 'some message ' + str(randint(0, 100)))
    producer.produce(topic=TOPIC_NAME, value=serializer(message), callback=delivery_report)
    producer.flush()
    logger.info('message sent')
    time.sleep(5)
