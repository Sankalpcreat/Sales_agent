from typing import Dict, Any, List
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DatabaseService:
    def __init__(self, db_url: str = 'sqlite:///sales_agent.db'):
        self.engine = sa.create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def store_lead(self, lead_data: Dict[str, Any], vector: List[float]) -> int:
        with self.Session() as session:
            try:
                lead_entry = Lead(**lead_data)
                session.add(lead_entry)
                session.commit()
                return lead_entry.id
            except Exception as e:
                session.rollback()
                raise

class Lead(Base):
    __tablename__ = 'leads'
    id = sa.Column(sa.Integer, primary_key=True)
    company_name = sa.Column(sa.String)
    industry = sa.Column(sa.String)
    source = sa.Column(sa.String)
    details = sa.Column(sa.JSON)

Base.metadata.create_all(sa.create_engine('sqlite:///sales_agent.db'))