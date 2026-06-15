from kafka import KafkaProducer

from datetime import datetime

import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TAG_NAME = "reactor_temp"

while True:

    now = datetime.now()

    value = round(
        random.uniform(70, 80),
        2
    )

    data = {
        "tag_name": TAG_NAME,
        "timestamp": now.isoformat(),
        "value": value
    }

    producer.send(
        "telemetry",
        data
    )

    producer.flush()

    print(data)

    time.sleep(5)