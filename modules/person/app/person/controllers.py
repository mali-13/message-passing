from datetime import datetime

from app.person.models import Person
from app.person.schemas import PersonSchema

from app.person.services import PersonService
from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

api = Namespace("UdaConnect Persons", description="Create and get Persons")  # noqa


# TODO: This needs better exception handling

@api.route("/person")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/person/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person
