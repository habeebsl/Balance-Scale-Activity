from sqlalchemy import Boolean, ForeignKey, Integer, String, Column, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base
import uuid


class User(Base):
    __tablename__ = 'users'
    uid = Column(String(128), primary_key=True, index=True)
    username = Column(String(50), nullable=True)
    email = Column(String(255), unique=True)
    role = Column(String(10), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    
    activities = relationship("Activity", back_populates="user")


class Activity(Base):
    __tablename__ = 'activities'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(50))
    last_modified = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    published = Column(Boolean, default=False)
    difficulty = Column(String(10))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    user_id = Column(String(128), ForeignKey('users.uid'))

    user = relationship("User", back_populates="activities")
    problemset = relationship("Problem", back_populates="activity", cascade="all, delete-orphan")


class Problem(Base):
    __tablename__ = 'problems'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    step = Column(Integer)
    target = Column(Integer)
    limit = Column(Integer)
    difficulty = Column(String(10))
    time_limit = Column(Integer, nullable=True)
    hint = Column(String(1000), nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    activity_id = Column(String(36), ForeignKey('activities.id'))

    activity = relationship("Activity", back_populates="problemset")