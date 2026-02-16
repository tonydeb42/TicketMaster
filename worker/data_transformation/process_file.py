from worker.worker import app
import pandas as pd
import boto3
import os
import redis
from dotenv import load_dotenv

load_dotenv()

def check_columns(df):
    required_columns = {"Employee ID", "Email", "Name", "Department", "Role/title", "Primary skills", "Secondary skills", "Experience years", "Problem domains handled"}
    missing_columns = required_columns - set(df.columns)
    return missing_columns

@app.task
def process_file(file_path):
    try:
        print(f"Processing file: {file_path}")

        s3 = boto3.client(
            "s3",
            endpoint_url=os.getenv("AWS_ENDPOINT_URL"),
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION_NAME")
        )

        obj = s3.get_object(Bucket=os.getenv("AWS_BUCKET"), Key=file_path)
        df = pd.read_csv(obj["Body"])

        missing_columns = check_columns(df)
        if missing_columns:
            raise ValueError(f"CSV file is missing required columns: {missing_columns}")

        print(f"Initial number of rows: {len(df)}")
        df.dropna(inplace=True)
        print(f"Number of rows after processing: {len(df)}")

        departments = df["Department"].unique()

        redis_client = redis.from_url(
            os.getenv("REDIS_HOST", "redis://localhost:6379/1"),
            decode_responses=True
        )       

        if not redis_client.exists("departments"):
            print("Creating departments set in Redis")

        redis_client.sadd("departments", *departments)

        df.to_csv(file_path, index=False)
        return file_path

    except Exception as e:
        print(f"Processing failed: {e}")
        raise e