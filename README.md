# Flutter Jobs Scraper with LangChain

A LangChain-powered job scraper that automatically finds Flutter developer jobs matching your criteria:
- **Remote positions**
- **Salary > 12 LPA** (Lakhs Per Annum)
- **Eligible for 2+ years experience**

The scraper uses AI (via LangChain and OpenAI) to intelligently extract and analyze job postings, then stores matching jobs in a local SQLite database.

## Features

- 🤖 **LangChain Integration**: Uses AI to intelligently extract job information
- 🎯 **Smart Filtering**: Automatically filters jobs by salary, experience, and location
- 💾 **Local Database**: Stores jobs in SQLite for offline access
- 🔄 **Duplicate Detection**: Prevents duplicate job entries
- 📊 **Detailed Logging**: Track scraping progress and results
- ⚙️ **Configurable**: Easy customization via `.env` file
- 🚀 **Server Ready**: Designed for deployment on your own server

## Project Structure

```
langchain_automation/
├── main.py                 # Main execution script
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── src/
    ├── database/         # Database models and operations
    │   ├── models.py     # SQLAlchemy models
    │   └── operations.py # Database CRUD operations
    ├── scrapers/         # Job scraping modules
    │   ├── base_scraper.py      # Base scraper class
    │   └── langchain_scraper.py # LangChain-powered scraper
    ├── filters/          # Job filtering logic
    │   └── job_filter.py # Filter implementation
    └── utils/            # Utility modules
        ├── config.py     # Configuration manager
        └── logger.py     # Logging setup
```

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for LangChain)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd langchain_automation
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```

5. **Edit `.env` file** and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Configuration

Edit the `.env` file to customize the scraper:

```env
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Database
DATABASE_PATH=./jobs.db

# Job Filtering Criteria
MIN_SALARY_LPA=12          # Minimum salary in Lakhs Per Annum
MIN_EXPERIENCE_YEARS=2     # Maximum experience for eligibility
JOB_KEYWORDS=flutter,Flutter,FLUTTER
REMOTE_ONLY=true           # Only include remote jobs

# Job Boards (comma-separated)
JOB_BOARDS=naukri.com,linkedin.com,indeed.co.in,instahyre.com
```

## Usage

### Basic Usage

Run the scraper:

```bash
python main.py
```

This will:
1. Initialize the database
2. Scrape Flutter jobs (currently uses sample data)
3. Filter jobs based on your criteria
4. Save matching jobs to the database
5. Display a summary of results

### Sample Output

```
============================================================
Flutter Jobs Scraper with LangChain
============================================================
Loading configuration...
Configuration: <Config(min_salary=12.0 LPA, min_exp=2.0 years, remote_only=True)>
Initializing database at: ./jobs.db
Database initialized successfully

============================================================
Starting job scraping...
============================================================

Total jobs found: 4

============================================================
Filtering jobs...
============================================================
✓ Flutter Developer at TechCorp India - Meets all criteria
✗ Senior Flutter Engineer at StartupXYZ - Meets all criteria
✗ Flutter Mobile Developer at FinTech Solutions - Not a remote position
✓ Flutter App Developer - Remote at Global Tech Inc - Meets all criteria

Jobs meeting criteria: 2/4

============================================================
Saving jobs to database...
============================================================
✓ Saved job: Flutter Developer at TechCorp India
✓ Saved job: Flutter App Developer - Remote at Global Tech Inc

============================================================
SUMMARY
============================================================
Total jobs scraped:     4
Jobs meeting criteria:  2
New jobs saved:         2
Duplicate/skipped:      0
Database location:      ./jobs.db
```

## Database Schema

The SQLite database stores jobs with the following fields:

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| title | String | Job title |
| company | String | Company name |
| location | String | Job location |
| is_remote | Boolean | Remote position flag |
| salary_min | Float | Minimum salary (LPA) |
| salary_max | Float | Maximum salary (LPA) |
| salary_currency | String | Currency (default: INR) |
| experience_min | Float | Minimum experience (years) |
| experience_max | Float | Maximum experience (years) |
| description | Text | Job description |
| skills | Text | Required skills |
| job_url | String | Job posting URL (unique) |
| source | String | Job board source |
| posted_date | DateTime | Job posting date |
| scraped_at | DateTime | When job was scraped |

## Extending the Scraper

### Adding Custom Job Boards

Edit `src/scrapers/langchain_scraper.py` and add URLs to the `scrape_flutter_jobs_generic` method:

```python
job_boards = [
    {
        'name': 'Naukri',
        'urls': ['https://www.naukri.com/flutter-jobs']
    },
    {
        'name': 'LinkedIn',
        'urls': ['https://www.linkedin.com/jobs/search/?keywords=flutter']
    },
]
```

### Customizing Filters

Edit `src/filters/job_filter.py` to modify filtering logic:

```python
def meets_criteria(self, job_data: Dict[str, Any]) -> tuple[bool, str]:
    # Add your custom filtering logic here
    pass
```

## Deployment on Server

### Using Cron for Automated Scraping

1. Make the script executable:
   ```bash
   chmod +x main.py
   ```

2. Add to crontab:
   ```bash
   crontab -e
   ```

3. Add a line to run daily at 9 AM:
   ```
   0 9 * * * cd /path/to/langchain_automation && /path/to/venv/bin/python main.py >> /path/to/logs/scraper.log 2>&1
   ```

### Using systemd Service

1. Create a service file `/etc/systemd/system/flutter-scraper.service`:
   ```ini
   [Unit]
   Description=Flutter Jobs Scraper
   After=network.target

   [Service]
   Type=simple
   User=your_user
   WorkingDirectory=/path/to/langchain_automation
   Environment="PATH=/path/to/venv/bin"
   ExecStart=/path/to/venv/bin/python main.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

2. Enable and start the service:
   ```bash
   sudo systemctl enable flutter-scraper.service
   sudo systemctl start flutter-scraper.service
   ```

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t flutter-scraper .
docker run -v $(pwd)/jobs.db:/app/jobs.db --env-file .env flutter-scraper
```

## Querying the Database

Use the provided database operations or SQLite directly:

### Python
```python
from src.database import get_all_jobs, get_jobs_by_criteria

# Get all jobs
jobs = get_all_jobs('./jobs.db')

# Get jobs with specific criteria
remote_jobs = get_jobs_by_criteria(
    min_salary=15,
    is_remote=True,
    max_experience=2,
    db_path='./jobs.db'
)
```

### SQLite CLI
```bash
sqlite3 jobs.db

# View all jobs
SELECT * FROM jobs;

# View remote jobs above 15 LPA
SELECT title, company, salary_min, salary_max
FROM jobs
WHERE is_remote = 1 AND salary_min >= 15;

# Count jobs by company
SELECT company, COUNT(*) as job_count
FROM jobs
GROUP BY company;
```

## Troubleshooting

### Issue: OpenAI API Error
**Solution**: Ensure your OpenAI API key is set correctly in `.env` file and has sufficient credits.

### Issue: No Jobs Found
**Solution**:
- Check job board URLs are accessible
- Verify network connectivity
- Review filter criteria (may be too restrictive)

### Issue: Database Locked
**Solution**:
- Close any other programs accessing the database
- Check file permissions
- Ensure only one scraper instance is running

## Best Practices

1. **Rate Limiting**: Add delays between requests to avoid being blocked
2. **User Agents**: Rotate user agents for better success rates
3. **Error Handling**: The scraper includes retry logic for failed requests
4. **Database Backups**: Regularly backup `jobs.db`
5. **API Costs**: Monitor OpenAI API usage to control costs

## Future Enhancements

- [ ] Add support for more job boards (Naukri, LinkedIn, Indeed)
- [ ] Implement email notifications for new matching jobs
- [ ] Create web dashboard for viewing jobs
- [ ] Add job application tracking
- [ ] Implement salary trend analysis
- [ ] Add support for other tech stacks

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Support

For issues and questions:
- Create an issue in the repository
- Check existing issues for solutions
- Review the troubleshooting section

## Acknowledgments

- Built with [LangChain](https://langchain.com/)
- Powered by [OpenAI](https://openai.com/)
- Database: [SQLAlchemy](https://www.sqlalchemy.org/)

---

**Happy Job Hunting! 🚀**
