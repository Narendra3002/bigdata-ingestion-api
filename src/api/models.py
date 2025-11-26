from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, DateTime, func
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    api_key = Column(String, unique=True)
    created_at = Column(TIMESTAMP)


class Credit(Base):
    __tablename__ = "credits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    credits_left = Column(Integer)
    last_updated = Column(TIMESTAMP)


class APILog(Base):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    endpoint = Column(String)
    query_params = Column(JSON)
    credits_used = Column(Integer)
    response_time_ms = Column(Integer)
    called_at = Column(TIMESTAMP)


class MasterData(Base):
    __tablename__ = "master_data"

    id = Column(Integer, primary_key=True, index=True)
    source_file = Column(String)
    raw_data = Column(JSON)
    normalized_data = Column(JSON)
    ingested_at = Column(TIMESTAMP, server_default=func.now())
class ContactsMaster(Base):
    __tablename__ = "contacts_master"

    id = Column(Integer, primary_key=True, index=True)

    source_file = Column(String(500))
    source_row_id = Column(String(100))

    person_name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))

    email = Column(String(320))
    phone = Column(String(50))

    city = Column(String(255))
    state = Column(String(255))
    country = Column(String(255))

    company = Column(String(255))
    job_title = Column(String(255))
    domain = Column(String(255))
    industry = Column(String(255))
    seniority_level = Column(String(100))
    experience_years = Column(Integer)

    linkedin_url = Column(String(500))
    facebook_url = Column(String(500))
    twitter_url = Column(String(500))

    raw_data = Column(JSONB)
    normalized_data = Column(JSONB)

    ingested_at = Column(DateTime, server_default=func.now())