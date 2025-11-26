import time
from sqlalchemy.orm import Session
from .models import APILog

def log_api_call(
    db: Session,
    user_id: int,
    endpoint: str,
    query_params: dict,
    credits_used: int,
    start_time: float
):
    duration_ms = int((time.time() - start_time) * 1000)

    log_row = APILog(
        user_id=user_id,
        endpoint=endpoint,
        query_params=query_params,
        credits_used=credits_used,
        response_time_ms=duration_ms
    )
    db.add(log_row)
    db.commit()
