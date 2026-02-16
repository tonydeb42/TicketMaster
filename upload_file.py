import boto3

s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)

# Create bucket
s3.create_bucket(Bucket="ticketmaster")

# Upload file
s3.upload_file("./data/employees_data.csv", "ticketmaster", "employees_data.csv")

print(s3.list_buckets())
