import grpc
from app.connection.gRPC.person_pb2 import PersonRequest
from app.connection.gRPC.person_pb2_grpc import PersonServiceStub


def get_persons(person_ids):
    with grpc.insecure_channel('person-api:50051') as channel:
        stub = PersonServiceStub(channel)
        response = stub.GetPersons(PersonRequest(person_ids=person_ids))
        persons = [map_to_person(person) for person in response.persons]
        return persons

def map_to_person(person):
    return {
        "id": person.id,
        "first_name": person.first_name,
        "last_name": person.last_name,
        "company_name": person.company_name
    }

