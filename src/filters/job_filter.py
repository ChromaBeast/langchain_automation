import re
from typing import Dict, Any, Optional


class JobFilter:
    """Filter jobs based on criteria"""

    def __init__(self, min_salary_lpa=12, max_experience_years=2, remote_only=True):
        """
        Initialize job filter

        Args:
            min_salary_lpa: Minimum salary in LPA (Lakhs Per Annum)
            max_experience_years: Maximum experience required for eligibility
            remote_only: Only include remote jobs
        """
        self.min_salary_lpa = min_salary_lpa
        self.max_experience_years = max_experience_years
        self.remote_only = remote_only

    def meets_criteria(self, job_data: Dict[str, Any]) -> tuple[bool, str]:
        """
        Check if job meets all criteria

        Args:
            job_data: Dictionary containing job information

        Returns:
            Tuple of (meets_criteria: bool, reason: str)
        """
        # Check remote requirement
        if self.remote_only and not job_data.get('is_remote', False):
            return False, "Not a remote position"

        # Check salary requirement
        salary_min = job_data.get('salary_min')
        if salary_min is None:
            return False, "Salary information not available"

        if salary_min < self.min_salary_lpa:
            return False, f"Salary {salary_min} LPA is below minimum {self.min_salary_lpa} LPA"

        # Check experience requirement
        experience_min = job_data.get('experience_min')
        if experience_min is None:
            # If no minimum experience specified, assume it's entry-level friendly
            return True, "Meets all criteria"

        if experience_min > self.max_experience_years:
            return False, f"Minimum experience {experience_min} years exceeds eligibility {self.max_experience_years} years"

        return True, "Meets all criteria"

    @staticmethod
    def extract_salary_from_text(text: str) -> Optional[tuple[float, float]]:
        """
        Extract salary range from text

        Args:
            text: Text containing salary information

        Returns:
            Tuple of (min_salary, max_salary) in LPA, or None
        """
        if not text:
            return None

        # Patterns for LPA (Lakhs Per Annum)
        lpa_patterns = [
            r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:lpa|LPA|lakh)',
            r'(\d+(?:\.\d+)?)\s*(?:lpa|LPA|lakh)',
            r'₹\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*(?:L|lakhs?)',
            r'(\d+)L\s*-\s*(\d+)L',
        ]

        for pattern in lpa_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return float(match.group(1)), float(match.group(2))
                else:
                    salary = float(match.group(1))
                    return salary, salary

        return None

    @staticmethod
    def extract_experience_from_text(text: str) -> Optional[tuple[float, float]]:
        """
        Extract experience range from text

        Args:
            text: Text containing experience information

        Returns:
            Tuple of (min_experience, max_experience) in years, or None
        """
        if not text:
            return None

        # Patterns for experience
        exp_patterns = [
            r'(\d+)\s*-\s*(\d+)\s*(?:years?|yrs?)',
            r'(\d+)\+?\s*(?:years?|yrs?)',
            r'minimum\s*(\d+)\s*(?:years?|yrs?)',
        ]

        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    return float(match.group(1)), float(match.group(2))
                else:
                    exp = float(match.group(1))
                    return exp, exp + 2  # Assume +2 years range

        return None

    @staticmethod
    def is_remote_job(text: str) -> bool:
        """
        Check if job is remote based on text

        Args:
            text: Text to check for remote indicators

        Returns:
            True if remote, False otherwise
        """
        if not text:
            return False

        remote_keywords = [
            r'\bremote\b',
            r'\bwork from home\b',
            r'\bwfh\b',
            r'\banywhere\b',
            r'\bdistributed\b',
        ]

        text_lower = text.lower()
        for keyword in remote_keywords:
            if re.search(keyword, text_lower):
                return True

        return False

    @staticmethod
    def is_flutter_job(text: str) -> bool:
        """
        Check if job is related to Flutter

        Args:
            text: Text to check for Flutter keywords

        Returns:
            True if Flutter-related, False otherwise
        """
        if not text:
            return False

        flutter_keywords = [
            r'\bflutter\b',
            r'\bdart\b',
            r'\bflutter developer\b',
            r'\bflutter engineer\b',
        ]

        text_lower = text.lower()
        for keyword in flutter_keywords:
            if re.search(keyword, text_lower):
                return True

        return False
