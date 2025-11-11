from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Job(Base):
    """Job model for storing scraped job listings"""
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False)
    company = Column(String(300), nullable=False)
    location = Column(String(300))
    is_remote = Column(Boolean, default=False)
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_currency = Column(String(10), default='INR')
    experience_min = Column(Float)
    experience_max = Column(Float)
    description = Column(Text)
    skills = Column(Text)  # Comma-separated skills
    job_url = Column(String(1000), unique=True)
    source = Column(String(100))  # Job board source
    posted_date = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Job(title='{self.title}', company='{self.company}', salary_min={self.salary_min})>"

    def to_dict(self):
        """Convert job object to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'is_remote': self.is_remote,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'salary_currency': self.salary_currency,
            'experience_min': self.experience_min,
            'experience_max': self.experience_max,
            'description': self.description,
            'skills': self.skills,
            'job_url': self.job_url,
            'source': self.source,
            'posted_date': self.posted_date,
            'scraped_at': self.scraped_at
        }


def init_db(db_path='./jobs.db'):
    """Initialize the database"""
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session(), engine


def get_session(db_path='./jobs.db'):
    """Get database session"""
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    return Session()
