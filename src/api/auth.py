# src/api/auth.py
from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, Credit

def _extract_api_key_from_request(request: Request) -> str | None:
    # check common header names
    for h in ("x-api-key", "api-key", "api_key", "authorization"):
        if h in request.headers:
            return request.headers[h]
    return None

def authenticate(request: Request, db: Session = Depends(get_db)):
    api_key = _extract_api_key_from_request(request)
    if not api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    # if Authorization: Bearer TOKEN, support that too
    if api_key.lower().startswith("bearer "):
        api_key = api_key.split(" ", 1)[1].strip()

    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    credit = db.query(Credit).filter(Credit.user_id == user.id).first()
    if not credit or credit.credits_left <= 0:
        raise HTTPException(status_code=402, detail="Insufficient credits")

    return user, credit
