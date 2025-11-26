# 📘 Unified Master Schema — Big Data Contacts

## 1. Master Table: `contacts_master`

| Column       | Type     | Description |
|--------------|----------|-------------|
| id           | BIGINT   | Unique record ID |
| person_name  | TEXT     | Full name of the person |
| email        | TEXT     | Email address |
| phone        | TEXT     | Phone number |
| city         | TEXT     | City name |
| state        | TEXT     | State name |
| country      | TEXT     | Country |
| company      | TEXT     | Company name |
| job_title    | TEXT     | Job title or profession |

---

## 2. Schema Decisions (Normalization)

### ✔ Master Schema Fields
All incoming datasets are normalized into the following fields:
- `person_name`
- `email`
- `phone`
- `city`
- `state`
- `country`
- `company`
- `job_title`

### ✔ Duplicate Removal Strategy
Duplicates are identified using:
(email, phone)

If both are null → row is included but flagged with lower priority.

---

## 3. Input Formats Supported

| Format  | Handled By |
|---------|------------|
| CSV     | Pandas, Python CSV |
| TSV     | Pandas `sep="\t"` |
| Excel   | Pandas `read_excel` |
| JSON    | `json` module / Pandas |
| JSONL   | Line-by-line parser |

---

## 4. Example of Unified Record

```json
{
  "id": 1636215,
  "person_name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+1-202-555-1234",
  "city": "New York",
  "state": "NY",
  "country": "USA",
  "company": "Example Corp",
  "job_title": "Project Manager"
}
5. Ingestion Output Workflow
Raw → Normalized → Deduped → Inserted
| Stage      | File/Output           |
| ---------- | --------------------- |
| Raw Input  | raw_input.*           |
| Normalized | normalized_output.csv |
| Deduped    | unique_contacts.csv   |
| Database   | contacts_master table |
6. Database Indexes
CREATE INDEX idx_country ON contacts_master(country);
CREATE INDEX idx_email ON contacts_master(email);
CREATE INDEX idx_phone ON contacts_master(phone);
CREATE INDEX idx_company ON contacts_master(company);
Indexes drastically improve query performance when dataset size grows beyond 50M+ records.
7. Future Expansion
The schema supports:

Adding hashed email/phone for privacy

Adding more enrichment fields (LinkedIn, domain, etc.)

Partitioning by country for large datasets

---

# 👉 **NEXT STEP FOR YOU**
1. Open this file:

2. Paste the full content above  
3. Save  
4. Then run:

```bash
git add docs/schema/schema-definition.md
git commit -m "Add schema-definition.md documentation"
git push
