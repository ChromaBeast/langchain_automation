#!/usr/bin/env python3
"""
Flutter Jobs Scraper with LangChain
Scrapes Flutter dev jobs, filters by criteria (remote, >12 LPA, 2yr exp), and saves to local database
"""

import sys
import os
from typing import List, Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import init_db, save_job, get_all_jobs
from src.filters import JobFilter
from src.scrapers import LangChainJobScraper
from src.utils import Config, setup_logger


def main():
    """Main execution function"""

    # Setup logger
    logger = setup_logger()

    logger.info("=" * 60)
    logger.info("Flutter Jobs Scraper with LangChain")
    logger.info("=" * 60)

    # Load configuration
    logger.info("Loading configuration...")
    config = Config()

    # Validate configuration
    is_valid, errors = config.validate()
    if not is_valid:
        logger.error("Configuration errors:")
        for error in errors:
            logger.error(f"  - {error}")
        sys.exit(1)

    logger.info(f"Configuration: {config}")

    # Initialize database
    logger.info(f"Initializing database at: {config.database_path}")
    try:
        session, engine = init_db(config.database_path)
        session.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        sys.exit(1)

    # Initialize job filter
    logger.info("Initializing job filter...")
    job_filter = JobFilter(
        min_salary_lpa=config.min_salary_lpa,
        max_experience_years=config.min_experience_years,
        remote_only=config.remote_only
    )

    # Initialize scraper
    logger.info("Initializing LangChain job scraper with Gemini...")
    try:
        scraper = LangChainJobScraper(api_key=config.google_api_key)
        logger.info("Scraper initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize scraper: {str(e)}")
        sys.exit(1)

    # Scrape jobs
    logger.info("\n" + "=" * 60)
    logger.info("Starting job scraping...")
    logger.info("=" * 60)

    all_jobs = []

    # For demonstration, we'll use sample jobs
    # In production, you can uncomment the line below to scrape real jobs
    # all_jobs = scraper.scrape_flutter_jobs_generic(keywords=config.job_keywords)

    logger.info("\nUsing sample jobs for demonstration...")
    logger.info("To scrape real jobs, you need to:")
    logger.info("  1. Implement specific job board scrapers")
    logger.info("  2. Or provide URLs to scrape")
    logger.info("  3. Uncomment the real scraping line in main.py")

    sample_jobs = scraper.create_sample_jobs()
    all_jobs.extend(sample_jobs)

    logger.info(f"\nTotal jobs found: {len(all_jobs)}")

    # Filter jobs
    logger.info("\n" + "=" * 60)
    logger.info("Filtering jobs...")
    logger.info("=" * 60)

    filtered_jobs = []
    for job in all_jobs:
        meets_criteria, reason = job_filter.meets_criteria(job)
        if meets_criteria:
            filtered_jobs.append(job)
            logger.info(f"✓ {job['title']} at {job['company']} - {reason}")
        else:
            logger.info(f"✗ {job['title']} at {job['company']} - {reason}")

    logger.info(f"\nJobs meeting criteria: {len(filtered_jobs)}/{len(all_jobs)}")

    # Save to database
    logger.info("\n" + "=" * 60)
    logger.info("Saving jobs to database...")
    logger.info("=" * 60)

    saved_count = 0
    skipped_count = 0

    for job in filtered_jobs:
        success, message = save_job(job, db_path=config.database_path)
        if success:
            saved_count += 1
            logger.info(f"✓ {message}")
        else:
            skipped_count += 1
            logger.info(f"○ {message}")

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total jobs scraped:     {len(all_jobs)}")
    logger.info(f"Jobs meeting criteria:  {len(filtered_jobs)}")
    logger.info(f"New jobs saved:         {saved_count}")
    logger.info(f"Duplicate/skipped:      {skipped_count}")
    logger.info(f"Database location:      {config.database_path}")

    # Display saved jobs
    logger.info("\n" + "=" * 60)
    logger.info("JOBS IN DATABASE")
    logger.info("=" * 60)

    all_saved_jobs = get_all_jobs(db_path=config.database_path)
    for idx, job in enumerate(all_saved_jobs, 1):
        logger.info(f"\n{idx}. {job['title']}")
        logger.info(f"   Company:    {job['company']}")
        logger.info(f"   Location:   {job['location']}")
        logger.info(f"   Remote:     {job['is_remote']}")
        logger.info(f"   Salary:     {job['salary_min']}-{job['salary_max']} LPA")
        logger.info(f"   Experience: {job['experience_min']}-{job['experience_max']} years")
        logger.info(f"   Skills:     {job['skills']}")
        logger.info(f"   URL:        {job['job_url']}")

    logger.info("\n" + "=" * 60)
    logger.info("Scraping completed successfully!")
    logger.info("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
