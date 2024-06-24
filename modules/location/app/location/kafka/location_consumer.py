from kafka import KafkaConsumer

import logging
from json import loads

from app.location.kafka.location_creator import LocationCreator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-api")


class LocationConsumer:
    consumer = KafkaConsumer('locations',
                             bootstrap_servers='10.43.52.231:9092',
                             value_deserializer=lambda x: loads(x.decode('utf-8')))

    location_creator = LocationCreator()
    for message in consumer:
        logger.info(message)
        location_creator.create(message.value)
