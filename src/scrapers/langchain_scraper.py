from typing import List, Dict, Any, Optional
import os
from langchain.agents import AgentType, initialize_agent, Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import requests
from bs4 import BeautifulSoup
import json
import re
from ..filters.job_filter import JobFilter


class LangChainJobScraper:
    """
    LangChain-powered job scraper that uses AI to extract and analyze job postings
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LangChain job scraper

        Args:
            api_key: Google API key (if not provided, reads from environment)
        """
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")

        # Initialize LLM with Gemini 2.5 Flash
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=self.api_key,
            temperature=0,
            convert_system_message_to_human=True
        )

        # Initialize job filter
        self.job_filter = JobFilter()

    def scrape_jobs_from_url(self, url: str, source: str = "custom") -> List[Dict[str, Any]]:
        """
        Scrape jobs from a specific URL using LangChain

        Args:
            url: URL to scrape
            source: Source name for the jobs

        Returns:
            List of extracted job dictionaries
        """
        try:
            # Fetch the page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text(separator=' ', strip=True)

            # Limit content to avoid token limits
            text_content = text_content[:8000]

            # Use LangChain to extract job information
            jobs = self._extract_jobs_with_langchain(text_content, url, source)
            return jobs

        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            return []

    def _extract_jobs_with_langchain(self, text: str, url: str, source: str) -> List[Dict[str, Any]]:
        """
        Use LangChain to extract job information from text

        Args:
            text: Text content to analyze
            url: Source URL
            source: Source name

        Returns:
            List of job dictionaries
        """
        prompt_template = """
        You are a job information extraction expert. Extract Flutter developer job information from the following text.

        Text:
        {text}

        Extract the following information for each Flutter developer job posting:
        - Job Title
        - Company Name
        - Location (mention if Remote/WFH)
        - Salary Range (in LPA if available)
        - Experience Required (in years)
        - Key Skills
        - Brief Description

        Format your response as a JSON array of job objects with these fields:
        - title
        - company
        - location
        - is_remote (boolean)
        - salary_min (number in LPA)
        - salary_max (number in LPA)
        - experience_min (number in years)
        - experience_max (number in years)
        - skills (comma-separated string)
        - description

        Only include Flutter-related jobs. If salary or experience is not mentioned, use null.
        Return ONLY the JSON array, no other text.
        """

        prompt = PromptTemplate(
            input_variables=["text"],
            template=prompt_template
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)

        try:
            result = chain.run(text=text)

            # Parse JSON result
            # Clean the result to extract JSON
            json_match = re.search(r'\[.*\]', result, re.DOTALL)
            if json_match:
                jobs_data = json.loads(json_match.group())
            else:
                jobs_data = json.loads(result)

            # Add metadata and validate
            validated_jobs = []
            for job in jobs_data:
                job['job_url'] = url
                job['source'] = source
                job['posted_date'] = None

                # Ensure required fields
                if job.get('title') and job.get('company'):
                    validated_jobs.append(job)

            return validated_jobs

        except json.JSONDecodeError as e:
            print(f"Error parsing LLM response: {str(e)}")
            return []
        except Exception as e:
            print(f"Error in LangChain extraction: {str(e)}")
            return []

    def scrape_flutter_jobs_generic(self, keywords: List[str] = None) -> List[Dict[str, Any]]:
        """
        Scrape Flutter jobs from popular Indian job boards

        Args:
            keywords: List of keywords (default: ['flutter'])

        Returns:
            List of job dictionaries
        """
        if keywords is None:
            keywords = ['flutter']

        all_jobs = []

        # Sample job board URLs (these are examples - in production, you'd construct search URLs)
        job_boards = [
            {
                'name': 'Instahyre',
                'urls': [
                    'https://www.instahyre.com/search-jobs/flutter/',
                ]
            },
            # Add more job boards as needed
        ]

        for board in job_boards:
            for url in board['urls']:
                print(f"Scraping {board['name']}: {url}")
                jobs = self.scrape_jobs_from_url(url, source=board['name'])
                all_jobs.extend(jobs)

        return all_jobs

    def create_sample_jobs(self) -> List[Dict[str, Any]]:
        """
        Create sample Flutter jobs for testing

        Returns:
            List of sample job dictionaries
        """
        sample_jobs = [
            {
                'title': 'Flutter Developer',
                'company': 'TechCorp India',
                'location': 'Remote',
                'is_remote': True,
                'salary_min': 15.0,
                'salary_max': 20.0,
                'salary_currency': 'INR',
                'experience_min': 2.0,
                'experience_max': 4.0,
                'description': 'Looking for a skilled Flutter developer to build cross-platform mobile applications.',
                'skills': 'Flutter, Dart, Firebase, REST APIs, Git',
                'job_url': 'https://example.com/job/1',
                'source': 'sample',
                'posted_date': None
            },
            {
                'title': 'Senior Flutter Engineer',
                'company': 'StartupXYZ',
                'location': 'Bangalore (Remote)',
                'is_remote': True,
                'salary_min': 18.0,
                'salary_max': 25.0,
                'salary_currency': 'INR',
                'experience_min': 1.5,
                'experience_max': 3.0,
                'description': 'Join our team to build innovative mobile solutions using Flutter.',
                'skills': 'Flutter, Dart, State Management, Firebase, CI/CD',
                'job_url': 'https://example.com/job/2',
                'source': 'sample',
                'posted_date': None
            },
            {
                'title': 'Flutter Mobile Developer',
                'company': 'FinTech Solutions',
                'location': 'Mumbai',
                'is_remote': False,
                'salary_min': 10.0,
                'salary_max': 14.0,
                'salary_currency': 'INR',
                'experience_min': 1.0,
                'experience_max': 3.0,
                'description': 'Develop cutting-edge fintech mobile applications.',
                'skills': 'Flutter, Dart, Payment Gateways, Security',
                'job_url': 'https://example.com/job/3',
                'source': 'sample',
                'posted_date': None
            },
            {
                'title': 'Flutter App Developer - Remote',
                'company': 'Global Tech Inc',
                'location': 'Remote (India)',
                'is_remote': True,
                'salary_min': 12.0,
                'salary_max': 16.0,
                'salary_currency': 'INR',
                'experience_min': 2.0,
                'experience_max': 4.0,
                'description': 'Build beautiful cross-platform applications for global clients.',
                'skills': 'Flutter, Dart, BLoC, Provider, REST APIs',
                'job_url': 'https://example.com/job/4',
                'source': 'sample',
                'posted_date': None
            },
        ]

        return sample_jobs
