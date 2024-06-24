import logging
import os

from typing import Dict
from app.location.models import Location
from app.location.schemas import LocationSchema
from geoalchemy2.functions import ST_Point

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("location-api")

class LocationCreator:
    def __init__(self):
        from app.config import config_by_name
        env = os.getenv("FLASK_ENV") or "test"
        config = config_by_name[env]

        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create(self, location: Dict) -> Location:
        validation_results: Dict = LocationSchema().validate(location)
        if validation_results:
            logger.warning(f"Unexpected data format in payload: {validation_results}")
            raise Exception(f"Invalid payload: {validation_results}")

        new_location = Location()
        new_location.person_id = location["person_id"]
        new_location.creation_time = location["creation_time"]
        new_location.coordinate = ST_Point(location["latitude"], location["longitude"])
        logger.info(f"""Adding ${new_location}""")
        self.session.add(new_location)
        self.session.commit()

        return new_location

