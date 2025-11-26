# Ingestion Pipeline Documentation

The ingestion system is designed to process large datasets from multiple formats and normalize them into the unified master schema.

## 1. Ingestion Scripts Available

### **1. ingest_csv.py**
- Handles CSV ingestion
- Reads large CSV files efficiently
- Cleans malformed rows
- Normalizes fields to unified schema
- Removes duplicates using `(email, phone)`
- Loads final cleaned data into `contacts_master` table (PostgreSQL)

### **2. ingest_all.py**
- Entry‑point script for ingesting multiple file formats
- Supports:
  - CSV
  - Excel (XLS/XLSX)
  - JSON
- Automatically detects file type
- Calls appropriate ingestion method
- Ensures deduplication and data normalization

---

## 2. Unified Schema (after ingestion)

All ingested files are converted to the following schema:

| Field | Description |
|-------|-------------|
| person_name | Full name of the person |
| email | Email address |
| phone | Phone number |
| city | City |
| state | State/Province |
| country | Country |
| company | Company |
| job_title | Job Title |

---

## 3. Deduplication Logic

A record is considered a duplicate if:

- **email AND phone match** another row  
- The first occurrence is kept

If both email & phone are missing → row is kept with low confidence.

---

## 4. Loading Into Database (PostgreSQL)

Final cleaned & normalized data is inserted into:


Indexes used for fast querying:

- email
- phone
- country
- company

---

## 5. How to Run the Ingestion

### Ingest ONLY CSV:

```bash
python ingest_csv.py
