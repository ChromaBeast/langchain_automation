from abc import ABC, abstractmethod
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import time


class BaseScraper(ABC):
    """Base class for job scrapers"""

    def __init__(self, headers=None):
        """
        Initialize the scraper

        Args:
            headers: Optional HTTP headers for requests
        """
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    @abstractmethod
    def scrape_jobs(self, keywords: List[str], **kwargs) -> List[Dict[str, Any]]:
        """
        Scrape jobs from the job board

        Args:
            keywords: List of keywords to search for
            **kwargs: Additional parameters

        Returns:
            List of job dictionaries
        """
        pass

    def fetch_page(self, url: str, retries=3, delay=2) -> str:
        """
        Fetch a page with retry logic

        Args:
            url: URL to fetch
            retries: Number of retries
            delay: Delay between retries in seconds

        Returns:
            Page content as string
        """
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    raise Exception(f"Failed to fetch {url}: {str(e)}")

    def parse_html(self, html_content: str) -> BeautifulSoup:
        """
        Parse HTML content

        Args:
            html_content: HTML string

        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html_content, 'html.parser')

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean text by removing extra whitespace

        Args:
            text: Text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""
        return ' '.join(text.split())
