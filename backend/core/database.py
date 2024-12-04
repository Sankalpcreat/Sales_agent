# backend/core/database.py
import os
from typing import Dict, Any, List
from datetime import datetime
import numpy as np

from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import ARRAY

# Use environment variable for database URL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:@localhost/sales_assistant_db')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for models
Base = declarative_base()

class LeadModel(Base):
    """Database model for storing lead suggestions"""
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    industry = Column(String)
    size_range = Column(String)
    pain_points = Column(String)
    opportunity_details = Column(JSON)
    vector = Column(ARRAY(Float), nullable=True)  # Store vector representation
    source = Column(String)
    confidence_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class MeetingSummaryModel(Base):
    """Database model for storing meeting summaries"""
    __tablename__ = "meeting_summaries"

    id = Column(Integer, primary_key=True, index=True)
    transcript = Column(String)
    summary = Column(String)
    key_participants = Column(JSON)
    discussion_points = Column(JSON)
    vector = Column(ARRAY(Float), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseService:
    """Database service for managing meeting summaries and leads"""
    
    def __init__(self, database_url: str = DATABASE_URL):
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def init_db(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """Create a new database session"""
        return self.SessionLocal()
    
    def store_lead(self, lead_data: Dict[str, Any], vector: np.ndarray = None):
        """Store lead suggestion in the database"""
        session = self.get_session()
        try:
            lead = LeadModel(**lead_data)
            if vector is not None:
                lead.vector = vector.tolist()
            session.add(lead)
            session.commit()
            return lead.id
        finally:
            session.close()
    
    def store_meeting_summary(self, summary_data: Dict[str, Any], vector: np.ndarray = None):
        """Store meeting summary in the database"""
        session = self.get_session()
        try:
            summary = MeetingSummaryModel(**summary_data)
            if vector is not None:
                summary.vector = vector.tolist()
            session.add(summary)
            session.commit()
            return summary.id
        finally:
            session.close()
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()

# Initialize database tables when module is imported
db_service = DatabaseService()
db_service.init_db()