from confluent_kafka import Consumer

from utils import TOPIC_NAME, MessageDeserializer

conf = {
    "bootstrap.servers": "localhost:9092",
    "auto.offset.reset": "earliest",
}

consumer = Consumer(conf,
                    enable_auto_commit=True,
                    fetch_min_bytes=1024
                    )

consumer.subscribe([TOPIC_NAME])

deserializer = MessageDeserializer()

try:
    while True:
        msg = consumer.poll(timeout=3)

        if msg is None:
            continue
        if msg.error():
            print(f'получена ошибка: {msg.error()}')
            continue

        msg = deserializer(msg)
        print(f'полученое сообщение: {msg.text} с заголовком {msg.header}')

except Exception as e:
    print(f'поймана ошибка: {e}')

finally:
    consumer.close()
