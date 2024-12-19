from confluent_kafka.serialization import Deserializer, Serializer

TOPIC_NAME = 'test-topic'


class Message:
    """
    Класс для сущности сообщение, которая имеет заголовок и текст
    """
    def __init__(self, header: str, text: str) -> None:
        self.header = header
        self.text = text


class MessageSerializer(Serializer):
    """
    Класс, используемый для сериализации сообщений типа Message
    """
    def __call__(self, obj: Message, ctx=None):
        header_bytes = obj.header.encode('utf-8')
        header_size = len(header_bytes)
        text_bytes = obj.text.encode('utf-8')
        text_size = len(text_bytes)

        result = header_size.to_bytes(4, byteorder='big')
        result += header_bytes
        result += text_size.to_bytes(4, byteorder='big')
        result += text_bytes

        print('message serizlized:', result)

        return result
    

class MessageDeserializer(Deserializer):
    """
    Класс, используемый для десериализации сообщений типа Message
    """
    def __call__(self, value: bytes, ctx: None):
        if value is None:
            return None
        
        header_size = int.from_bytes(value[0:4], byteorder='big')
        header_bytes = value[4:4+header_size]
        header = header_bytes.decode('utf-8')

        text_size = int.from_bytes(
            value[4+header_size:4+header_size+4],
            byteorder='big')
        text_bytes = value[4+header_size+4:4+header_size+4+text_size]
        text = text_bytes.decode('utf-8')

        return Message(header, text)


def delivery_report(err, msg):
    if err is not None:
        print(f'error when sending: {err}')
    else:
        print(f'message sent to {TOPIC_NAME}')
