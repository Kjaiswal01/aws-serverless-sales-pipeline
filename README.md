\# Event-Driven Serverless Sales Analytics Pipeline (AWS)



An end-to-end serverless data engineering pipeline built on AWS (`ap-south-1`) that automates ingestion, validation, transformation, SQL analytics, and visualization for retail sales data.



\## Architecture

`Local Python (boto3)` → `Amazon S3 (raw/)` → `AWS Lambda (ETL \& Validation)` → `Amazon S3 (processed/ \& failed/)` → `Amazon Athena (Serverless SQL)` → `Python Matplotlib Chart`



\## Project Structure

\- `src/etl\_pipeline.py` — Local pandas validation \& transformation script

\- `src/upload\_to\_s3.py` — Automated S3 ingestion script using `boto3`

\- `src/lambda\_function.py` — Serverless AWS Lambda event handler for validation \& quarantine

\- `src/visualize\_revenue.py` — Generates city-wise revenue bar charts from S3 processed data

\- `sql/athena\_analytics.sql` — Athena DDL (`CREATE EXTERNAL TABLE`) and analytical queries

\- `revenue\_by\_city.png` — Output revenue visualization

