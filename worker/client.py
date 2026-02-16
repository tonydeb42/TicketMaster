from worker.worker import app

# from worker.data_transformation.process_file import process_file
# from worker.data_transformation.create_embeddings import create_embeddings
# from worker.data_transformation.store_embeddings import store_embeddings
# from worker.data_transformation.send_notification import send_notification
# from worker.data_transformation.failure_notification import failure_notification

from worker.query_transformation.metadata_extractor import extract_metadata
from worker.query_transformation.query_parser import query_parser
from worker.query_transformation.retrieve_chunks import retrieve_chunks
from worker.query_transformation.generate_answer import generate_answer
from worker.query_transformation.send_notification import send_notification
from worker.query_transformation.failure_notification import failure_notification

from celery import chain
from celery.result import AsyncResult
import time
from dotenv import load_dotenv
import os

load_dotenv()

time.sleep(5)  # Wait for the worker to be ready

# file_upload_chain = chain(
#     process_file.s('employees_data.csv'),
#     create_embeddings.s(),
#     store_embeddings.s(),
#     send_notification.s('pratyushdeb70@gmail.com')
# ).apply_async(
#     link_error=failure_notification.s('pratyushdeb70@gmail.com')
# )

test = [
    {
        "query":"Kubernetes cluster experiencing OOMKilled errors, need to analyze memory usage with Prometheus and adjust resource limits.",
        "department":"Cloud Ops"
    },
    {
        "query":"React frontend build failing due to webpack configuration issues.",
        "department":"Marketing"
    },
    {
        "query":"Need to build a credit risk scoring model using historical loan data, experience with financial datasets required.",
        "department":"Data Science"
    },
    {
        "query":"Automate infrastructure provisioning on AWS using Terraform, set up monitoring with Prometheus, and configure Kubernetes cluster.",
        "department":"Cloud Ops"
    },
    {
        "query":"Debug legacy COBOL program on mainframe for banking transaction processing.",
        "department":"Engineering"
    }
]

find_employee_chain = chain(
    extract_metadata.s(test[3]["query"],test[3]["department"]),
    query_parser.s(),
    retrieve_chunks.s(),
    generate_answer.s(),
    send_notification.s('pratyushdeb70@gmail.com')
).apply_async(
    link_error=failure_notification.s('pratyushdeb70@gmail.com')
)

print("Task submitted, waiting for result...")

result = AsyncResult(find_employee_chain.id, app=app)
print(result.state)

while True:
    if result.ready():
        print(result.get())  
        break
    else:
        print(result.state)
        time.sleep(30)