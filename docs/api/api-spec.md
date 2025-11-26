# 📘 API Specification — Credit‑Based Big Data Contact API

Base URL:
http://127.0.0.1:8000


---

# 1. Authentication

Every request must include an API Key in headers:
api_key: YOUR_API_KEY

If invalid → API returns:

```json
{"error": "Invalid API Key"}
2. Endpoints
2.1 Health Check Endpoint
GET /
Used to check if server is running
Response
{"message": "Big Data + Credit API System Running"}
2.2 Protected Test Endpoint
GET /protected
Requires valid API Key

Deducts 1 credit

Response Example
{
  "message": "You accessed protected data!",
  "user": "Test User",
  "credits_left": 987
}
2.3 Contacts Search Endpoint
GET /contacts
Query Parameters:
| Param     | Type | Required | Description              |
| --------- | ---- | -------- | ------------------------ |
| page      | int  | No       | Page number (default: 1) |
| page_size | int  | No       | Items per page (1–200)   |
| country   | str  | No       | Filter by country        |
| email     | str  | No       | Filter by email          |
| phone     | str  | No       | Filter by phone          |
| company   | str  | No       | Filter by company        |
Credits Rule
Credits used = number of items returned

Example:

page_size=10 → 10 credits deducted

page_size=50 → 50 credits deducted

If credits insufficient:
{"error": "Insufficient Credits"}
Response Example
{
  "page": 1,
  "page_size": 10,
  "total": 1014052,
  "credits_used": 10,
  "credits_left": 988,
  "items": [
    {
      "id": 1636213,
      "email": "jlancaster@atmel.com",
      "phone": "408-441-0311",
      "country": "USA",
      "company": "Atmel Corp",
      "job_title": null
    }
  ]
}
3. Errors
Invalid API Key:
{"error": "Invalid API Key"}
Missing API Key:
{"error": "API Key Required"}
Not Enough Credits:
{"error": "Insufficient Credits"}
4. API Logging
Every API call is logged in api_logs:

Fields stored:

user_id

endpoint

query_params

credits_used

response_time_ms

called_at

Sample query:

SELECT * FROM api_logs ORDER BY id DESC LIMIT 5;
5. Rate Limit (Optional Future Enhancement)
Max 60 requests/min per user

Additional rules for high‑tier users


---

# 👉 **NEXT STEP FOR YOU**

1. Open the file:
docs/api/api-spec.md


2. Paste the full content above  
3. Save  
4. Run:

```bash
git add docs/api/api-spec.md
git commit -m "Add API specification documentation"
git push