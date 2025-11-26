# 📘 System Architecture — Big Data Ingestion + Credit‑Regulated API

## 1. Overview
This architecture supports:
- Ingestion of 70M–700M+ records from multiple formats
- Schema normalization and deduplication
- Scalable storage using PostgreSQL
- Fast credit‑regulated API using FastAPI
- API logging, authentication, pagination, and filtering

---

## 2. High‑Level Architecture Diagram

            ┌─────────────────────────┐
            │   External Data Files   │
            │ CSV / JSON / Excel etc │
            └──────────┬──────────────┘
                       │
                       ▼
          ┌───────────────────────────┐
          │  Ingestion Layer (Python) │
          │ - Schema detection         │
          │ - Cleaning, parsing        │
          │ - Normalization            │
          │ - Deduplication            │
          └──────────┬────────────────┘
                       │
                       ▼
      ┌───────────────────────────────────────┐
      │  Unified Storage Layer (PostgreSQL)   │
      │ - contacts_master table                │
      │ - indexing on email, phone, country    │
      └──────────┬────────────────────────────┘
                 │
                 ▼
  ┌──────────────────────────────────────────────┐
  │         API Layer (FastAPI + SQLAlchemy)     │
  │  - API Key authentication                    │
  │  - Credit deduction per request              │
  │  - Filtering (country, name, domain, etc.)   │
  │  - Pagination                                │
  └──────────┬───────────────────────────────────┘
             │
             ▼
 ┌──────────────────────────────────────────┐
 │        Logging & Credit System           │
 │ - api_logs table                         │
 │ - users & credits tables                 │
 └──────────────────────────────────────────┘

---

## 3. Ingestion Architecture

### Responsibilities:
✔ Multi‑format ingestion (CSV, Excel, JSON, TSV)  
✔ Schema normalization into common fields  
✔ Duplicate removal using `(email, phone)`  
✔ Batch insert into PostgreSQL

### Tools:
- Python
- Pandas
- Custom schema mapping
- PostgreSQL COPY for large inserts

---

## 4. Storage Architecture

### Database: PostgreSQL

Tables:
- `contacts_master`
- `users`
- `credits`
- `api_logs`

Indexes:
```sql
CREATE INDEX idx_country ON contacts_master(country);
CREATE INDEX idx_email ON contacts_master(email);
CREATE INDEX idx_phone ON contacts_master(phone);
5. API Architecture
Framework: FastAPI

Features:

Authentication using API Key

Credit deduction per request

Pagination

Filters: country, email, phone, company

Response metadata

6. Logging Architecture
api_logs stores:

user_id

endpoint

query_params

credits_used

response_time_ms

called_at

Used for billing and analytics.

7. Scalability Plan
Horizontal scaling via read replicas

PostgreSQL partitioning (range partition by country)

Redis caching for frequent queries

Sharding when dataset crosses 500M+

8. Deployment Architecture
Supports:

Docker containers

Docker Compose for local

Nginx reverse proxy

PostgreSQL container or managed DB

---

# ✅ NEXT STEP (Important)

After pasting the content:

### Run:

```bash
git add docs/architecture/architecture.md
git commit -m "Added architecture.md content"
git push
