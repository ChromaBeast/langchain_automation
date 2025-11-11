import os
from dotenv import load_dotenv
from typing import List


class Config:
    """Configuration manager for the job scraper"""

    def __init__(self, env_file='.env'):
        """
        Initialize configuration

        Args:
            env_file: Path to .env file
        """
        load_dotenv(env_file)

        # API Keys
        self.google_api_key = os.getenv('GOOGLE_API_KEY')

        # Database
        self.database_path = os.getenv('DATABASE_PATH', './jobs.db')

        # Scraping Configuration
        self.min_salary_lpa = float(os.getenv('MIN_SALARY_LPA', '12'))
        self.min_experience_years = float(os.getenv('MIN_EXPERIENCE_YEARS', '2'))
        self.job_keywords = os.getenv('JOB_KEYWORDS', 'flutter').split(',')
        self.remote_only = os.getenv('REMOTE_ONLY', 'true').lower() == 'true'

        # Job Boards
        job_boards_str = os.getenv('JOB_BOARDS', '')
        self.job_boards = [board.strip() for board in job_boards_str.split(',')] if job_boards_str else []

    def validate(self) -> tuple[bool, List[str]]:
        """
        Validate configuration

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        if not self.google_api_key:
            errors.append("GOOGLE_API_KEY is not set")

        if self.min_salary_lpa <= 0:
            errors.append("MIN_SALARY_LPA must be positive")

        if self.min_experience_years < 0:
            errors.append("MIN_EXPERIENCE_YEARS must be non-negative")

        return len(errors) == 0, errors

    def __repr__(self):
        return f"<Config(min_salary={self.min_salary_lpa} LPA, min_exp={self.min_experience_years} years, remote_only={self.remote_only})>"
