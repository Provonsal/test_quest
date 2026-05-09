from datetime import datetime, timezone

from sqlalchemy import TEXT, INTEGER, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, LargeBinary, ForeignKey, Text
from uuid import uuid4


Base = declarative_base()