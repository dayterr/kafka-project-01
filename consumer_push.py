import logging

from confluent_kafka import Consumer

from utils import GROUP_ID, TOPIC_NAME, MessageDeserializer

logger = logging.getLogger(__name__)
logger.info('push consumer started')

conf = {
    "group.id": GROUP_ID,
    "bootstrap.servers": "127.0.0.1:9094,127.0.0.1:9095,127.0.0.1:9096",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": "false",
    "fetch.min.bytes": 1024,
}

consumer = Consumer(conf)

consumer.subscribe([TOPIC_NAME])

deserializer = MessageDeserializer()

try:
    while True:
        msg = consumer.poll(timeout=0)

        if msg is None:
            continue
        if msg.error():
            logger.error(f'получена ошибка: {msg.error()}')
            continue

        msg = deserializer(msg.value())
        consumer.commit(asynchronous=False)
        logger.info(f'полученое сообщение: {msg.text} с заголовком {msg.header}')

except Exception as e:
    logger.error(f'поймана ошибка: {e}')

finally:
    consumer.close()
