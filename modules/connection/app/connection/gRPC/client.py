import grpc
from .person_pb2 import person_pb2
from .person_pb2_grpc import person_pb2_grpc

from ..models import Person

def get_persons(person_ids):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = person_pb2_grpc.PersonServiceStub(channel)
        response = stub.GetPersons(person_pb2.PersonRequest(person_ids=person_ids))
        persons = [map_to_person(person) for person in response.persons]
        return persons

def map_to_person(person):
    return Person(
        id=person.id,
        first_name=person.first_name,
        last_name=person.last_name,
        company_name=person.company_name
    )

if __name__ == '__main__':
    print('Helo!')

