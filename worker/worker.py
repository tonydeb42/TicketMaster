from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

app = Celery('ticketmaster_worker', 
             broker=os.getenv('CELERY_BROKER_URL'),
             backend=os.getenv('CELERY_BACKEND_URL'))

app.conf.update(
    CELERY_IMPORTS=(
        'worker.data_transformation.process_file',
        'worker.data_transformation.create_embeddings',
        'worker.data_transformation.store_embeddings',
        'worker.data_transformation.send_notification',
        'worker.data_transformation.failure_notification',
        'worker.query_transformation.metadata_extractor',
        'worker.query_transformation.query_parser',
        'worker.query_transformation.retrieve_chunks',
        'worker.query_transformation.generate_answer',
        'worker.query_transformation.send_notification',
        'worker.query_transformation.failure_notification',
    )
)