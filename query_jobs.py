#!/usr/bin/env python3
"""
Query script to view jobs in the database
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import get_all_jobs, get_jobs_by_criteria
from src.utils import Config
import argparse


def display_job(job, index=None):
    """Display a single job"""
    prefix = f"{index}. " if index else ""
    print(f"\n{prefix}{job['title']}")
    print(f"   Company:     {job['company']}")
    print(f"   Location:    {job['location']}")
    print(f"   Remote:      {job['is_remote']}")
    print(f"   Salary:      {job['salary_min']}-{job['salary_max']} LPA")
    print(f"   Experience:  {job['experience_min']}-{job['experience_max']} years")
    print(f"   Skills:      {job['skills']}")
    print(f"   URL:         {job['job_url']}")
    print(f"   Source:      {job['source']}")
    print(f"   Scraped:     {job['scraped_at']}")


def main():
    parser = argparse.ArgumentParser(description='Query Flutter jobs from database')
    parser.add_argument('--min-salary', type=float, help='Minimum salary in LPA')
    parser.add_argument('--remote', action='store_true', help='Only remote jobs')
    parser.add_argument('--max-experience', type=float, help='Maximum experience required')
    parser.add_argument('--db', default='./jobs.db', help='Database path')

    args = parser.parse_args()

    print("=" * 60)
    print("Flutter Jobs Database Query")
    print("=" * 60)

    if args.min_salary or args.remote or args.max_experience:
        print(f"\nFilters:")
        if args.min_salary:
            print(f"  Min Salary: {args.min_salary} LPA")
        if args.remote:
            print(f"  Remote Only: Yes")
        if args.max_experience:
            print(f"  Max Experience: {args.max_experience} years")

        jobs = get_jobs_by_criteria(
            min_salary=args.min_salary,
            is_remote=args.remote if args.remote else None,
            max_experience=args.max_experience,
            db_path=args.db
        )
    else:
        print("\nShowing all jobs")
        jobs = get_all_jobs(db_path=args.db)

    print(f"\nFound {len(jobs)} job(s)")
    print("=" * 60)

    for idx, job in enumerate(jobs, 1):
        display_job(job, idx)

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
