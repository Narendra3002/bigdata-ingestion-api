# 📘 Credit System Documentation — Big Data API

## 1. Overview
The system uses a **credit‑based access model** to control how many API requests a user can make.

Every user has:
- A unique API key  
- A credit balance  
- A complete usage log  

When credits reach **0**, the API blocks further access.

---

## 2. Database Tables

### 🟦 users
Stores user details + API Key.

| Column | Type | Description |
|--------|------|-------------|
| id     | int  | Primary key |
| name   | text | User name |
| api_key | text | Secret API key |

---

### 🟩 credits
Stores credit balance for each user.

| Column | Type | Description |
|--------|------|-------------|
| user_id | int | Linked to users.id |
| credits_left | int | Number of credits remaining |

---

### 🟧 api_logs
Stores every API call.

| Column | Type | Description |
|--------|------|-------------|
| id | int | Primary key |
| user_id | int | Caller | 
| endpoint | text | Endpoint accessed |
| query_params | jsonb | Filters used |
| credits_used | int | Credits deducted |
| response_time_ms | int | API latency |
| called_at | timestamp | Time of call |

---

## 3. How Credits Are Deducted

### Contacts API Rule:
credits_used = number_of_items_returned


Examples:
- page_size=10 → costs 10 credits  
- page_size=50 → costs 50 credits  

### Protected Endpoint Rule:
credits_used = 1


### When credits become zero:
```json
{"error": "Insufficient Credits"}
4. Admin Credit Management
Admin can add credits using SQL:

UPDATE credits
SET credits_left = credits_left + 500
WHERE user_id = 1;
Set initial credits:

INSERT INTO credits (user_id, credits_left)
VALUES (1, 1000);
5. Logging & Auditing
Admins can monitor usage:

SELECT * FROM api_logs ORDER BY id DESC LIMIT 20;
This helps:

billing

fraud detection

usage analytics

performance tracking

6. Future Credit Features (Optional)
Daily credit refill

Tiered pricing

Rate limiting

Credit usage dashboard


---

# ✅ **NOW DO THIS:**

After pasting, run:

```bash
git add docs/credit/credit-system.md
git commit -m "Add credit system documentation"
git push