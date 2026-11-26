import boto3

BUCKET_NAME = "cloud-sales-datalake-kshitij-2026"
LOCAL_FILE = "data/raw/sales_day2.csv"
S3_KEY = "raw/sales_day2.csv"

s3 = boto3.client("s3")
s3.upload_file(LOCAL_FILE, BUCKET_NAME, S3_KEY)
print(f"Uploaded {LOCAL_FILE} to s3://{BUCKET_NAME}/{S3_KEY}")
