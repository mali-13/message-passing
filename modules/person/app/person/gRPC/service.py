from concurrent import futures
import grpc
import person_pb2
import person_pb2_grpc

from ..models import Person
from ..services import PersonService

class PersonService(person_pb2_grpc.PersonServiceServicer):

    def GetPersons(self, request, context):
        persons = PersonService.retrieve_by_ids(request.person_ids)
        response = person_pb2.PersonResponse()
        for person in persons:
            response.persons.add(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name
            )
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    person_pb2_grpc.add_PersonServiceServicer_to_server(PersonService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
