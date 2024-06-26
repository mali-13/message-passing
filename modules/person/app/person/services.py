import logging
from datetime import datetime, timedelta
from typing import Dict, List

from app import db
from app.person.models import Person

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("person-api")

class PersonService:
    @staticmethod
    def create(person: Dict) -> Person:
        new_person = Person()
        new_person.first_name = person["first_name"]
        new_person.last_name = person["last_name"]
        new_person.company_name = person["company_name"]

        db.session.add(new_person)
        db.session.commit()

        return new_person

    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = db.session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return db.session.query(Person).all()

    @staticmethod
    def retrieve_by_ids(person_ids: List[int]) -> List[Person]:
        return db.session.query(Person).filter(Person.id.in_(person_ids)).all()
