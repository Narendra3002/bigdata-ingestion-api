from fastapi import FastAPI, Depends, Query, Header, HTTPException
from sqlalchemy.orm import Session
import time

from .database import engine, get_db
from .models import Base, ContactsMaster
from .auth import authenticate
from .logging_utils import log_api_call

app = FastAPI(title="Big Data + Credit API System")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Big Data + Credit API System Running"}


# 🔐 Protected endpoint example (uses credits)
@app.get("/contacts")
def list_contacts(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),

    name: str | None = Query(None, description="Search in person_name"),
    email: str | None = Query(None, description="Search in email"),
    company: str | None = Query(None, description="Search in company"),
    country: str | None = Query(None, description="Filter by country"),

    api_key: str = Header(None),
    user_data: tuple = Depends(authenticate),
    db: Session = Depends(get_db),
):
    start_time = time.time()

    user, credit = user_data

    # Build base query
    q = db.query(ContactsMaster)

    if name:
        q = q.filter(ContactsMaster.person_name.ilike(f"%{name}%"))
    if email:
        q = q.filter(ContactsMaster.email.ilike(f"%{email}%"))
    if company:
        q = q.filter(ContactsMaster.company.ilike(f"%{company}%"))
    if country:
        q = q.filter(ContactsMaster.country.ilike(f"%{country}%"))

    total = q.count()

    skip = (page - 1) * page_size

    rows = (
        q.order_by(ContactsMaster.id)
         .offset(skip)
         .limit(page_size)
         .all()
    )

    data = []
    for c in rows:
        data.append(
            {
                "id": c.id,
                "person_name": c.person_name,
                "email": c.email,
                "phone": c.phone,
                "city": c.city,
                "state": c.state,
                "country": c.country,
                "company": c.company,
                "job_title": c.job_title,
            }
        )

    # 🔢 Credits logic: 1 credit per contact returned
    credits_used = len(data)

    if credit.credits_left < credits_used:
        # not enough credits
        raise HTTPException(
            status_code=402,
            detail="Not enough credits to fetch this many contacts",
        )

    credit.credits_left -= credits_used
    db.commit()

    # 🧾 Log this API call
    query_params = {
        "page": page,
        "page_size": page_size,
        "name": name,
        "email": email,
        "company": company,
        "country": country,
    }

    log_api_call(
        db=db,
        user_id=user.id,
        endpoint="/contacts",
        query_params=query_params,
        credits_used=credits_used,
        start_time=start_time,
    )

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "credits_used": credits_used,
        "credits_left": credit.credits_left,
        "items": data,
    }

