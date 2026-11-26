\# Event-Driven Serverless Sales Analytics Pipeline (AWS)



An end-to-end, serverless cloud data engineering pipeline built on \*\*AWS (`ap-south-1` / Mumbai)\*\* that automates daily retail sales ingestion, data quality validation, error quarantine, serverless SQL analytics, and revenue visualization—with \*\*₹0 idle compute cost\*\*.



\---



\## System Architecture \& Data Flow



```text

+-----------------------+       +-----------------------------------+

|   Local Machine       |       |           Amazon S3               |

|  (Python + boto3)     | ----> |   (Data Lakehouse - ap-south-1)   |

|  upload\_to\_s3.py      |       |                                   |

+-----------------------+       |  \[ raw/sales\_day\*.csv ]           |

&#x20;                               +-----------------+-----------------+

&#x20;                                                 |

&#x20;                                   S3 ObjectCreated Event (\*.csv)

&#x20;                                                 v

&#x20;                               +-----------------------------------+

&#x20;                               |           AWS Lambda              |

&#x20;                               |      (sales-etl-processor)        |

&#x20;                               |  - Validate qty > 0 \& price > 0   |

&#x20;                               |  - Calculate total\_amount         |

&#x20;                               |  - Standardize city names         |

&#x20;                               +--------+-----------------+--------+

&#x20;                                        |                 |

&#x20;                            Valid Rows  |                 | Invalid Rows

&#x20;                                        v                 v

&#x20;                       +------------------------+  +------------------------+

&#x20;                       |  S3: processed/        |  |  S3: failed/           |

&#x20;                       |  cleaned\_sales\_\*.csv   |  |  failed\_sales\_\*.csv    |

&#x20;                       +------------+-----------+  +------------------------+

&#x20;                                    |

&#x20;                     Schema-on-Read | (External Table)

&#x20;                                    v

&#x20;                       +------------------------+

&#x20;                       |     Amazon Athena      |

&#x20;                       |  (Serverless SQL DB)   |

&#x20;                       |  sales\_analytics\_db    |

&#x20;                       +------------+-----------+

&#x20;                                    |

&#x20;                        boto3 / CSV | Aggregation

&#x20;                                    v

&#x20;                       +------------------------+

&#x20;                       | Python Visualization   |

&#x20;                       | (pandas + matplotlib)  |

&#x20;                       | revenue\_by\_city.png    |

&#x20;                       +------------------------+

```



\### Visual Flow (GitHub Flowchart)

```mermaid

flowchart LR

&#x20;   A\[Local Python<br/>boto3 Ingestion] -->|Uploads CSV| B\[(Amazon S3<br/>raw/ Zone)]

&#x20;   B -->|S3 Event Trigger| C\[AWS Lambda<br/>ETL \& Data Validation]

&#x20;   C -->|Valid Records| D\[(Amazon S3<br/>processed/ Zone)]

&#x20;   C -->|Malformed Records| E\[(Amazon S3<br/>failed/ Quarantine)]

&#x20;   D -->|Schema-on-Read| F\[Amazon Athena<br/>Serverless SQL Analytics]

&#x20;   F -->|Aggregated Metrics| G\[Matplotlib Dashboard<br/>revenue\_by\_city.png]

```



\---



\## Output Visualization

!\[Total Sales Revenue by City](revenue\_by\_city.png)



\---



\## End-to-End Workflow Breakdown



1\. \*\*Automated Ingestion (`src/upload\_to\_s3.py`):\*\* Uses `boto3` and IAM credentials to push daily raw CSV batches into the `raw/` landing zone of Amazon S3.

2\. \*\*Event-Driven Serverless ETL (`src/lambda\_function.py`):\*\* An S3 `ObjectCreated` trigger (filtered strictly to prefix `raw/` and suffix `.csv` to prevent recursive loops) automatically invokes AWS Lambda (`Python 3.12`).

3\. \*\*Data Quality \& Quarantine Pattern:\*\*

&#x20;  - \*\*Valid records\*\* (`quantity > 0` and numeric `price > 0`) get enriched with `total\_amount = quantity \* price`, have city names normalized (`.strip().title()`), and are written to `processed/`.

&#x20;  - \*\*Malformed records\*\* (negative/zero quantities or missing prices) are isolated into `failed/` so bad data never corrupts downstream analytics.

4\. \*\*Serverless SQL Analytics (`sql/analytics\_queries.sql`):\*\* Amazon Athena queries all multi-day CSV files inside `processed/` directly via a `CREATE EXTERNAL TABLE` definition (`skip.header.line.count = 1`), computing city-wise and category-wise revenue with zero database servers.

5\. \*\*BI Visualization (`src/visualize\_revenue.py`):\*\* Fetches processed datasets via `boto3` and generates `revenue\_by\_city.png` using `pandas` and `matplotlib`.



\---



\## Repository Structure

```text

aws-serverless-sales-pipeline/

├── data/

│   ├── raw/                  # Incoming daily sales batches (sales\_day1.csv, sales\_day2.csv)

│   ├── processed/            # Validated \& enriched sales records

│   ├── failed/               # Quarantined records failing validation rules

│   └── city\_revenue.csv      # Exported Athena SQL aggregation

├── sql/

│   └── analytics\_queries.sql # Athena DDL \& business intelligence SQL queries

├── src/

│   ├── etl\_pipeline.py       # Local pandas ETL prototype

│   ├── upload\_to\_s3.py       # Automated S3 ingestion via boto3

│   ├── lambda\_function.py    # Serverless AWS Lambda ETL \& validation handler

│   └── visualize\_revenue.py  # Automated revenue chart generator

├── revenue\_by\_city.png       # City-wise revenue bar chart

├── .gitignore

└── README.md

```

