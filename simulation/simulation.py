from kafka import KafkaProducer

from datetime import datetime

import json
import random
import time
import logging

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

logging.basicConfig(
    filename="/logs/simulation.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    force=True
)

logger = logging.getLogger("simulation")
TAG_NAME = "reactor_temp"

while True:
    ts_now = now.isoformat()
    now = datetime.now()
    day = ts.strftime("%Y-%m-%d")
    value = round(
        random.uniform(70, 80),
        2
    )

    data = {
        "tag_name": TAG_NAME,
        "timestamp": ts_now,
        "value": value
    }
    try:
        producer.send(
            "telemetry",
            data
        )

        producer.flush()

        logging.info(
                json.dumps({
                    "event": "simulation_input",
                    "source": "simulation",
                    "tag_name": TAG_NAME,
                    "value": value,
                    "day": day,
                    "status": "success",
                    "timestamp": ts_now
                })
            )
    except Exception as e:
        
        logging.error(
        json.dumps({
            "event":"simulation_input",
            "status":"error",
            "tag_name":TAG_NAME,
            "error":str(e)
        })
    )    

    time.sleep(5)