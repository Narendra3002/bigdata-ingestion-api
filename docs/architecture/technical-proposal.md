# Technical Proposal — Unified Big Data Ingestion, Storage & Credit‑Regulated API

## 1. Problem Statement

This system is designed to:

- Ingest large and heterogeneous datasets (70M–200M+, scalable toward 700M+)
- Normalize inconsistent schemas into one unified contacts model
- Store data efficiently in a scalable database (PostgreSQL)
- Expose data via a secure, credit‑controlled API
- Support filtering, pagination, logging, and monitoring

The focus is scalability, performance, and ease of deployment.

---

## 2. Technology Choices

### Python
- Excellent for data processing
- Rich libraries for ingestion (csv, pandas)
- Easy integration with APIs

### FastAPI
- High‑performance async framework
- Built‑in validation & automatic docs
- Perfect for scalable REST APIs

### PostgreSQL
- Strong relational engine for structured data
- Indexing & partitioning support
- Can scale with read replicas or Citus extension

### Docker & Kubernetes
- Containerization for consistent deployment
- Kubernetes for future scaling and orchestration

---

## 3. Architecture Overview

### Ingestion Layer
- Reads CSV/Excel/JSON files
- Normalizes fields:
  `person_name, email, phone, city, state, country, company, job_title`
- Removes duplicates using `(email, phone)`
- Loads into `contacts_master`

### Storage Layer
- PostgreSQL tables:
  - `contacts_master`
  - `users`
  - `credits`
  - `api_logs`
- Indexes for fast filtering:
  - email, phone, country, company

### API Layer (FastAPI)
- Endpoints:
  - `/`
  - `/protected`
  - `/contacts`
- Handles filtering, pagination, credit deduction, logging

### Credit System
- API key authentication
- Credits stored in DB
- Deduction per request based on items fetched

### Logging Layer
- Each API call logged in `api_logs`
- Contains query params, credits, response time

---

## 4. Scalability

Short‑term:
- Indexes for fast queries
- Efficient pagination

Long‑term:
- Horizontal API scaling (Kubernetes replicas)
- PostgreSQL partitioning
- Optional Redis cache
- Sharding via Citus for 700M+ records

---

## 5. Security

- API key authentication
- Credits prevent abuse
- Secrets stored in `.env`
- HTTPS recommended for deployment
- DB access restricted to internal network

---

## 6. Deployment Strategy

### Local:
- `docker-compose.yml` starts:
  - FastAPI container
  - PostgreSQL container

### Cloud / Kubernetes:
- Deployment manifests
- NodePort for exposing API
- ClusterIP for DB
- Horizontal scaling possible

---

## 7. Conclusion

The system is scalable, secure, documented, and meets the assignment requirements for a unified big data ingestion pipeline and credit‑regulated API delivery system.
