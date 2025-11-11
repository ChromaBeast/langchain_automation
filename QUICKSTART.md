# Quick Start Guide

Get started with the Flutter Jobs Scraper in 5 minutes!

## 1. Prerequisites

- Python 3.8+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd langchain_automation

# Run setup script
bash setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 3. Configuration

Edit `.env` file and add your OpenAI API key:

```env
OPENAI_API_KEY=your_key_here
```

## 4. Run

```bash
# Activate virtual environment (if not already)
source venv/bin/activate

# Run the scraper
python main.py
```

## 5. View Results

```bash
# View all jobs
python query_jobs.py

# View only remote jobs with min 15 LPA
python query_jobs.py --remote --min-salary 15

# View jobs requiring max 2 years experience
python query_jobs.py --max-experience 2
```

## 6. Database

Jobs are stored in `jobs.db` SQLite database:

```bash
# Query with SQLite
sqlite3 jobs.db "SELECT title, company, salary_min FROM jobs;"
```

## Production Deployment

### Option 1: Cron Job

```bash
# Edit crontab
crontab -e

# Add daily job at 9 AM
0 9 * * * cd /path/to/langchain_automation && /path/to/venv/bin/python main.py
```

### Option 2: Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## Customization

Edit `.env` file to customize:

```env
MIN_SALARY_LPA=12          # Change minimum salary
MIN_EXPERIENCE_YEARS=2     # Change experience requirement
REMOTE_ONLY=true          # Set to false to include office jobs
```

## Need Help?

- Read the full [README.md](README.md)
- Check [Troubleshooting](#troubleshooting) section
- Open an issue on GitHub

## Next Steps

1. Add real job board URLs to scraper
2. Set up automated scheduling
3. Configure email notifications
4. Customize filtering criteria

Happy job hunting! 🚀
