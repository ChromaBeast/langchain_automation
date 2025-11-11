from sqlalchemy.exc import IntegrityError
from .models import Job, get_session
import os
from datetime import datetime


def save_job(job_data, db_path='./jobs.db'):
    """
    Save a job to the database

    Args:
        job_data: Dictionary containing job information
        db_path: Path to the database file

    Returns:
        Tuple of (success: bool, message: str)
    """
    Session = get_session(db_path)
    session = Session()

    try:
        # Check if job already exists
        existing_job = session.query(Job).filter_by(job_url=job_data.get('job_url')).first()
        if existing_job:
            session.close()
            return False, f"Job already exists: {job_data.get('title')}"

        # Create new job
        job = Job(
            title=job_data.get('title'),
            company=job_data.get('company'),
            location=job_data.get('location'),
            is_remote=job_data.get('is_remote', False),
            salary_min=job_data.get('salary_min'),
            salary_max=job_data.get('salary_max'),
            salary_currency=job_data.get('salary_currency', 'INR'),
            experience_min=job_data.get('experience_min'),
            experience_max=job_data.get('experience_max'),
            description=job_data.get('description'),
            skills=job_data.get('skills'),
            job_url=job_data.get('job_url'),
            source=job_data.get('source'),
            posted_date=job_data.get('posted_date'),
            scraped_at=datetime.utcnow()
        )

        session.add(job)
        session.commit()
        session.close()
        return True, f"Saved job: {job_data.get('title')} at {job_data.get('company')}"

    except IntegrityError as e:
        session.rollback()
        session.close()
        return False, f"Database integrity error: {str(e)}"
    except Exception as e:
        session.rollback()
        session.close()
        return False, f"Error saving job: {str(e)}"


def job_exists(job_url, db_path='./jobs.db'):
    """Check if a job already exists in the database"""
    Session = get_session(db_path)
    session = Session()

    exists = session.query(Job).filter_by(job_url=job_url).first() is not None
    session.close()
    return exists


def get_all_jobs(db_path='./jobs.db'):
    """Get all jobs from the database"""
    Session = get_session(db_path)
    session = Session()

    jobs = session.query(Job).all()
    job_list = [job.to_dict() for job in jobs]
    session.close()
    return job_list


def get_jobs_by_criteria(min_salary=None, is_remote=None, max_experience=None, db_path='./jobs.db'):
    """Get jobs matching specific criteria"""
    Session = get_session(db_path)
    session = Session()

    query = session.query(Job)

    if min_salary:
        query = query.filter(Job.salary_min >= min_salary)

    if is_remote is not None:
        query = query.filter(Job.is_remote == is_remote)

    if max_experience:
        query = query.filter(Job.experience_min <= max_experience)

    jobs = query.all()
    job_list = [job.to_dict() for job in jobs]
    session.close()
    return job_list
