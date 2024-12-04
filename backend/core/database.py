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
    """
    Comprehensive database model for storing lead suggestions
    """
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
    """
    Database model for storing meeting summaries
    """
    __tablename__ = "meeting_summaries"

    id = Column(Integer, primary_key=True, index=True)
    transcript = Column(String)
    summary = Column(String)
    key_participants = Column(JSON)
    discussion_points = Column(JSON)
    action_items = Column(JSON)
    vector = Column(ARRAY(Float), nullable=True)
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class DatabaseService:
    """
    Centralized database service for managing data persistence
    """
    def __init__(self, database_url: str = DATABASE_URL):
        """
        Initialize database connection and session
        """
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def init_db(self):
        """
        Create all database tables
        """
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self) -> Session:
        """
        Create a new database session
        """
        return self.SessionLocal()
    
    def store_lead(self, lead_data: Dict[str, Any], vector: np.ndarray = None):
        """
        Store lead suggestion in the database
        
        :param lead_data: Dictionary of lead information
        :param vector: Optional vector representation of the lead
        """
        session = self.get_session()
        try:
            # Convert numpy vector to list if provided
            vector_list = vector.tolist() if vector is not None else None
            
            lead = LeadModel(
                company_name=lead_data.get('company_name', 'Unknown'),
                industry=lead_data.get('industry', 'Unknown'),
                size_range=lead_data.get('size_range', 'Unknown'),
                pain_points=lead_data.get('pain_points', 'Unknown'),
                opportunity_details=lead_data.get('opportunity_details', {}),
                vector=vector_list,
                source=lead_data.get('source', 'system'),
                confidence_score=lead_data.get('confidence_score', 0.0)
            )
            
            session.add(lead)
            session.commit()
            return lead.id
        except Exception as e:
            session.rollback()
            print(f"Error storing lead: {e}")
            return None
        finally:
            session.close()
    
    def store_meeting_summary(self, summary_data: Dict[str, Any], vector: np.ndarray = None):
        """
        Store meeting summary in the database
        
        :param summary_data: Dictionary of meeting summary information
        :param vector: Optional vector representation of the summary
        """
        session = self.get_session()
        try:
            # Convert numpy vector to list if provided
            vector_list = vector.tolist() if vector is not None else None
            
            summary = MeetingSummaryModel(
                transcript=summary_data.get('transcript', ''),
                summary=summary_data.get('summary', ''),
                key_participants=summary_data.get('key_participants', {}),
                discussion_points=summary_data.get('discussion_points', {}),
                action_items=summary_data.get('action_items', {}),
                vector=vector_list,
                source=summary_data.get('source', 'system')
            )
            
            session.add(summary)
            session.commit()
            return summary.id
        except Exception as e:
            session.rollback()
            print(f"Error storing meeting summary: {e}")
            return None
        finally:
            session.close()
    
    def close(self):
        """
        Close database connection
        """
        self.engine.dispose()

# Initialize database tables when module is imported
db_service = DatabaseService()
db_service.init_db()