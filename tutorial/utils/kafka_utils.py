from kafka import KafkaProducer
from json import dumps


class KProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=lambda x: dumps(x).encode("utf-8"),
        )

    def produce(self, topic_name, data):
        print("sending data to kafka topic "+str(topic_name))
        self.producer.send(topic_name, value=data)

        
        
        
