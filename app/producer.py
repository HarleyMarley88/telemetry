from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers="localhost:9092"
)

producer.send(
    "telemetry",
    b"Hello Kafka"
)

producer.flush()

print("Message sent")