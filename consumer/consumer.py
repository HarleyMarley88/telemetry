from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from datetime import datetime
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge

import json
import logging
import threading
import time

logging.basicConfig(
    filename="/logs/consumer.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    force=True
)

KAFKA_LAG = Gauge("kafka_consumer_lag", "Kafka consumer lag")

MESSAGES_RECEIVED = Counter(
    "messages_received_total",
    "Total received messages"
)
ERRORS_TOTAL = Counter(
    "consumer_errors_total",
    "Total consumer errors"
)
TEMPERATURE = Gauge(
    "reactor_temperature",
    "Current reactor temperature"
)
logger = logging.getLogger("telemetry")

logger.info("Consumer started")

cluster = Cluster(["cassandra"])

session = cluster.connect("demo")

start_http_server(8001)

consumer = KafkaConsumer(
    "telemetry",
    bootstrap_servers="kafka:9092",
    auto_offset_reset="latest",
    group_id="telemetry-group"
)


for msg in consumer:


    data = json.loads(
        msg.value.decode()
    )
    MESSAGES_RECEIVED.inc()
    tag_name = data["tag_name"]

    value = data["value"]
    TEMPERATURE.set(value)
    ts = datetime.fromisoformat(
        data["timestamp"]
    )
    
    day = ts.strftime("%Y-%m-%d")
    try:
        session.execute(
            """
            INSERT INTO tag_history_v2
            (tag_name, day, ts, value)
            VALUES (%s, %s, %s, %s)
            """,
            (
                tag_name,
                day,
                ts,
                value
            )
        )

        logging.info(
            json.dumps({
                "event": "telemetry_saved",
                "source": "consumer",
                "tag_name": tag_name,
                "value": value,
                "day": day,
                "status": "success",
                "timestamp": ts.isoformat()
            })
        )
        
    except Exception as e:
        ERRORS_TOTAL.inc()
        logging.error(
        json.dumps({
            "event":"telemetry_saved",
            "status":"error",
            "tag_name":tag_name,
            "error":str(e)
        })
    )

def calculate_lag():
    partitions = consumer.partitions_for_topic("telemetry")
    end_offsets = consumer.end_offsets(partitions)

    committed = {
        p: consumer.committed(p)
        for p in partitions
    }

    lag = 0

    for p in partitions:
        if committed[p] is not None:
            lag += end_offsets[p] - committed[p]

    return lag        

def update_lag():
    while True:
        lag = calculate_lag()
        KAFKA_LAG.set(lag)
        time.sleep(5)

threading.Thread(target=update_lag, daemon=True).start()        