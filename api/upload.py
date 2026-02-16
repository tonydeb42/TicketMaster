from fastapi import APIRouter, UploadFile, File, HTTPException
import boto3
import botocore
import uuid
from api.models.UploadSuccess import UploadSuccess

from celery import chain
from worker.data_transformation.process_file import process_file
from worker.data_transformation.create_embeddings import create_embeddings
from worker.data_transformation.store_embeddings import store_embeddings
from worker.data_transformation.send_notification import send_notification
from worker.data_transformation.failure_notification import failure_notification

from dotenv import load_dotenv
import os

load_dotenv()
upload_router = APIRouter()

email = os.getenv("NOTIFICATION_EMAIL")

@upload_router.post("/", response_model=UploadSuccess)
async def upload_file(file: UploadFile = File(...)):
    try:
        file_extension = os.path.splitext(file.filename)[1].lower()
        if(file_extension not in ['.csv']):
            raise HTTPException(status_code=400, detail="Invalid file type. Only CSV files are allowed.")
        
        s3 = boto3.client(
        "s3",
        endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION_NAME")
        )
        try:
            s3.head_bucket(Bucket="ticketmaster")
        except botocore.exceptions.ClientError:
            s3.create_bucket(Bucket="ticketmaster")
        filename = f"{uuid.uuid4()}_{file.filename}"
        s3.upload_fileobj(file.file, "ticketmaster", filename)

        current_user = email

        file_upload_chain = chain(
            process_file.s(filename),
            create_embeddings.s(),
            store_embeddings.s(),
            send_notification.s(current_user)
        ).apply_async(
            link_error=failure_notification.s(current_user)
        )

        return {"status": "success", "message": "File uploaded and processing started."}
    except Exception as e:
        print(f"File upload failed: {e}")
        raise HTTPException(status_code=500, detail="File upload failed: " + str(e))