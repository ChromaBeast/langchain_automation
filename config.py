#!/usr/bin/env python3
"""
Configuration file for Flutter Jobs Scraper
Customize these values according to your requirements
"""

# Job Filtering Criteria
MIN_SALARY_LPA = 12  # Minimum salary in Lakhs Per Annum
MAX_EXPERIENCE_YEARS = 2  # Maximum experience required (for 2yr exp person eligibility)
REMOTE_ONLY = True  # Only include remote jobs

# Keywords to search for
JOB_KEYWORDS = ['flutter', 'Flutter', 'FLUTTER', 'Dart']

# Database Configuration
DATABASE_PATH = './jobs.db'

# Job Boards to Scrape (URLs can be added here)
JOB_BOARD_URLS = [
    # Add specific job board URLs here
    # Example:
    # 'https://www.naukri.com/flutter-jobs',
    # 'https://www.linkedin.com/jobs/search/?keywords=flutter',
]

# Scraping Settings
REQUEST_DELAY = 2  # Delay between requests in seconds
MAX_RETRIES = 3  # Maximum number of retries for failed requests
TIMEOUT = 10  # Request timeout in seconds

# Logging
LOG_LEVEL = 'INFO'  # Options: DEBUG, INFO, WARNING, ERROR
LOG_FILE = None  # Set to a file path to enable file logging
