# Big Data Ingestion & Credit‑Based API System

This project implements a unified Big Data ingestion + credit‑regulated API system.  
It supports:
- Multi‑format ingestion (CSV, Excel, JSON, TSV)
- Schema normalization into a common contact model
- PostgreSQL storage
- FastAPI backend with:
  - API key authentication
  - Credit deduction per request
  - Pagination + filtering
  - Full API logging

## Features
### 🔹 Big Data Ingestion (Design)
- Normalize to master schema
- Clean inconsistent fields
- Remove duplicates using (email, phone)

### 🔹 Storage Layer
- PostgreSQL `contacts_master` table
- Indexed for fast search (`country`, `email`, `phone`, `company`)

### 🔹 Credit‑Based API
- API key per user
- Credits stored in `credits` table
- `/contacts` consumes credits = items returned
- All calls logged in `api_logs`

## API Summary
- `GET /` → Health check
- `GET /protected` → Costs 1 credit
- `GET /contacts` → Supports filters + pagination

## Project Structure
bigdata-ingestion-api/
├── src/ (FastAPI app)
├── docs/
│   ├── architecture/
│   ├── schema/
│   ├── api/
│   └── credit/
└── README.md

