import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.connection.models import Connection, Location, Person
from sqlalchemy.sql import text

from app.connection.gRPC.client import get_persons

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("connection-api")


class ConnectionService:
    @staticmethod
    def find_contacts2(person_id: int, start_date: datetime, end_date: datetime, meters=5
    ) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        # Prepare arguments for queries
        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )

        exposed_locations = sum([db.engine.execute(query, **line) for line in tuple(data)], [])
        exposed_person_ids = [exposed_person_id for exposed_person_id in exposed_locations]
        exposed_persons = get_persons(exposed_person_ids)
        exposed_person_map = {person['person_id']: person for person in exposed_persons}


        result: List[Connection] = []
        for (
            exposed_person_id,
            location_id,
            exposed_lat,
            exposed_long,
            exposed_time,
        ) in exposed_locations:
            location = Location(
                id=location_id,
                person_id=exposed_person_id,
                creation_time=exposed_time,
            )
            location.set_wkt_with_coords(exposed_lat, exposed_long)

            result.append(
                Connection(
                    person=exposed_person_map[exposed_person_id], location=location,
                )
            )

        return result

    @staticmethod
    def find_contacts(person_id: int, start_date: datetime, end_date: datetime, meters=5) -> List[Connection]:
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        print(
            f"Finding contacts for person_id: {person_id}, start_date: {start_date}, end_date: {end_date}, meters: {meters}")

        locations: List = db.session.query(Location).filter(
            Location.person_id == person_id
        ).filter(Location.creation_time < end_date).filter(
            Location.creation_time >= start_date
        ).all()

        print(f"Found {len(locations)} locations")

        # Prepare arguments for queries
        data = []
        for location in locations:
            data.append(
                {
                    "person_id": person_id,
                    "longitude": location.longitude,
                    "latitude": location.latitude,
                    "meters": meters,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": (end_date + timedelta(days=1)).strftime("%Y-%m-%d"),
                }
            )

        query = text(
            """
        SELECT  person_id, id, ST_X(coordinate), ST_Y(coordinate), creation_time
        FROM    location
        WHERE   ST_DWithin(coordinate::geography,ST_SetSRID(ST_MakePoint(:latitude,:longitude),4326)::geography, :meters)
        AND     person_id != :person_id
        AND     TO_DATE(:start_date, 'YYYY-MM-DD') <= creation_time
        AND     TO_DATE(:end_date, 'YYYY-MM-DD') > creation_time;
        """
        )

        print(f"Executing query for {len(data)} locations")

        exposed_locations = sum([db.engine.execute(query, **line) for line in tuple(data)], [])
        print(f"Found {len(exposed_locations)} exposed locations")

        exposed_person_ids = [exposed_person_id for exposed_person_id in exposed_locations]

        print(f"Found {len(exposed_person_ids)} exposed person IDs")
        print(f"Example exposed person ID: {exposed_person_ids[0]}")  # Print an example ID

        exposed_persons = get_persons(exposed_person_ids)

        print(f"Found {len(exposed_persons)} exposed persons")
        print(f"Example exposed person: {exposed_persons[0]}")

        exposed_person_map = {person['person_id']: person for person in exposed_persons}

        print(f"Created exposed person map with {len(exposed_person_map)} persons")

        result: List[Connection] = []
        for (
                exposed_person_id,
                location_id,
                exposed_lat,
                exposed_long,
                exposed_time,
        ) in exposed_locations:
            location = Location(
                id=location_id,
                person_id=exposed_person_id,
                creation_time=exposed_time,
            )
            location.set_wkt_with_coords(exposed_lat, exposed_long)

            print(f"Adding connection for exposed person_id: {exposed_person_id}")

            result.append(
                Connection(
                    person=exposed_person_map[exposed_person_id], location=location,
                )
            )

        print(f"Returning {len(result)} connections")

        return result