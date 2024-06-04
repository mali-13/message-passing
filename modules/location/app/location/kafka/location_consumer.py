from kafka import KafkaConsumer

import logging


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("location-api")


class LocationConsumer:
    TOPIC_NAME = 'locations'
    consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers='10.43.52.231:9092')

    for message in consumer:
        logger.info(message)
