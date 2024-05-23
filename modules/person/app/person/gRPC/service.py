import logging
from concurrent import futures
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import grpc
from app.person.gRPC.person_pb2 import PersonResponse
from app.person.gRPC.person_pb2_grpc import add_PersonServiceServicer_to_server, PersonServiceServicer

from app.person.models import Person

from typing import List

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("person-gRPC")

class GRPCPersonService(PersonServiceServicer):

    def __init__(self):
        from app.config import config_by_name
        env = os.getenv("FLASK_ENV") or "test"
        config = config_by_name[env]

        self.engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def GetPersons(self, request, context):
        logging.info("Received request to get persons with IDs: %s", request.person_ids)
        persons = self.retrieve_by_ids(request.person_ids)
        response = PersonResponse()
        for person in persons:
            response.persons.add(
                id=person.id,
                first_name=person.first_name,
                last_name=person.last_name,
                company_name=person.company_name
            )
        return response


    def retrieve_by_ids(self, person_ids: List[int]) -> List[Person]:
        return self.session.query(Person).filter(Person.id.in_(person_ids)).all()

def serve():
    # Configure logging (adjust level and filename as needed)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PersonServiceServicer_to_server(GRPCPersonService(), server)
    server.add_insecure_port('[::]:50051')
    logger.info("Starting gRPC server on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
