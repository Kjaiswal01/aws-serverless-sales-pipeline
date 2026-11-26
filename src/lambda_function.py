import boto3
import csv
import io
import os
import urllib.parse

s3 = boto3.client("s3")

def lambda_handler(event, context):
    # 1. Extract bucket name and uploaded file key from the S3 event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    raw_key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"])

    # Safety check: only process CSV files inside raw/
    if not raw_key.startswith("raw/") or not raw_key.endswith(".csv"):
        print(f"Skipping non-target file: {raw_key}")
        return {"status": "skipped"}

    filename = os.path.basename(raw_key)
    print(f"Processing s3://{bucket}/{raw_key}")

    # 2. Download raw CSV content into memory
    response = s3.get_object(Bucket=bucket, Key=raw_key)
    raw_content = response["Body"].read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(raw_content))

    valid_rows = []
    failed_rows = []
    
    raw_headers = reader.fieldnames or []
    processed_headers = raw_headers + ["total_amount"]

    # 3. Validate & transform row by row
    for row in reader:
        try:
            qty = float(row.get("quantity", ""))
            price = float(row.get("price", ""))
            
            if qty <= 0 or price <= 0:
                failed_rows.append(row)
                continue

            # Transform: calculate total_amount and standardize city
            clean_row = dict(row)
            clean_row["city"] = clean_row.get("city", "").strip().title()
            clean_row["total_amount"] = round(qty * price, 2)
            valid_rows.append(clean_row)

        except (ValueError, TypeError):
            # Catches null, empty, or non-numeric quantity/price
            failed_rows.append(row)

    # 4. Write valid rows to processed/
    if valid_rows:
        valid_buf = io.StringIO()
        writer = csv.DictWriter(valid_buf, fieldnames=processed_headers)
        writer.writeheader()
        writer.writerows(valid_rows)
        s3.put_object(
            Bucket=bucket,
            Key=f"processed/cleaned_{filename}",
            Body=valid_buf.getvalue()
        )

    # 5. Write failed rows to failed/
    if failed_rows:
        failed_buf = io.StringIO()
        writer = csv.DictWriter(failed_buf, fieldnames=raw_headers)
        writer.writeheader()
        writer.writerows(failed_rows)
        s3.put_object(
            Bucket=bucket,
            Key=f"failed/failed_{filename}",
            Body=failed_buf.getvalue()
        )

    summary = f"Processed {filename}: {len(valid_rows)} valid, {len(failed_rows)} failed."
    print(summary)
    return {"status": "success", "summary": summary}