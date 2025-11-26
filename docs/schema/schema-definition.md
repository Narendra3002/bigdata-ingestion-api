# 📘 Unified Master Schema — Big Data Contacts

## 1. Master Table: `contacts_master`

| Column       | Type     | Description |
|--------------|----------|-------------|
| id           | BIGINT   | Unique record ID |
| person_name  | TEXT     | Full name of the person |
| email        | TEXT     | Email address |
| phone        | TEXT     | Phone number |
| city         | TEXT     | City name |
| state        | TEXT     | State/Province |
| country      | TEXT     | Country |
| company      | TEXT     | Company or Organization |
| job_title    | TEXT     | Job title or designation |

---

## 2. Schema Normalization Rules

All incoming files (CSV, Excel, JSON, TSV) are mapped into a **unified schema**.

### Input Field Examples:
- `Name`, `FullName`, `person`, `contact_name` → `person_name`
- `E-mail`, `mail`, `emailAddress` → `email`
- `mobile`, `contact_number`, `telephone` → `phone`

### Standardized Output:
person_name
email
phone
city
state
country
company
job_title

---

## 3. Duplicate Removal Strategy

Duplicate rows are detected using:


If both email & phone are NULL → record is kept (marked low confidence).

---

## 4. Supported Input Formats

| Format  | Method Used |
|---------|-------------|
| CSV     | pandas.read_csv |
| TSV     | pandas.read_csv (sep="\t") |
| Excel   | pandas.read_excel |
| JSON    | json module / pandas |
| JSONL   | line-by-line parser |
| SQL dump | custom import + regex parsing |

---

## 5. Example of Unified Record

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
6. Output Pipeline Stages
| Stage        | Description                     |
| ------------ | ------------------------------- |
| Raw Input    | Original file from dataset      |
| Normalized   | Unified field mapping completed |
| Cleaned      | Bad rows fixed/removed          |
| Deduped      | Duplicate records removed       |
| Final Output | Inserted into `contacts_master` |
CREATE INDEX idx_country ON contacts_master(country);
CREATE INDEX idx_email ON contacts_master(email);
CREATE INDEX idx_phone ON contacts_master(phone);
CREATE INDEX idx_company ON contacts_master(company);
8. Future Schema Extensions
hashed_email, hashed_phone (privacy)

linkedin_url, domain, industry

enrichments from 3rd party APIs


---

# 👉 **When pasted, run:**

```bash
git add docs/schema/schema-definition.md
git commit -m "Add schema-definition.md"
git push