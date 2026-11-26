import boto3
import pandas as pd
import matplotlib.pyplot as plt
import io

BUCKET_NAME = "cloud-sales-datalake-kshitij-2026"
s3 = boto3.client("s3")

# Fetch all cleaned CSV files directly from S3 processed/
objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="processed/").get("Contents", [])
dfs = []
for obj in objects:
    if obj["Key"].endswith(".csv"):
        body = s3.get_object(Bucket=BUCKET_NAME, Key=obj["Key"])["Body"].read().decode("utf-8")
        dfs.append(pd.read_csv(io.StringIO(body)))

df = pd.concat(dfs, ignore_index=True)
city_rev = df.groupby("city")["total_amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 4))
city_rev.plot(kind="bar", color="#2b5c8f")
plt.title("Total Sales Revenue by City (INR)")
plt.xlabel("City")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("revenue_by_city.png")
print("Saved chart to revenue_by_city.png")