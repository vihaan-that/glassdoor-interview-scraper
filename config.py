# Configuration file for Glassdoor Interview Scraper
# Copy this file and update with your settings

# ========================
# API CONFIGURATION
# ========================

# Google Generative AI (Gemini) API Key
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = "your-gemini-api-key-here"

# Preferred Gemini model (options: gemini-2.0-flash-exp, gemini-1.5-pro, gemini-1.5-flash)
GEMINI_MODEL = "gemini-2.0-flash-exp"

# ========================
# SCRAPING CONFIGURATION
# ========================

# Browser settings
BROWSER_CONFIG = {
    "headless": False,  # Set to True for headless browsing
    "block_images": True,  # Block images for faster loading
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "window_size": (1920, 1080)
}

# Scraping limits
MAX_PAGES = 10  # Maximum pages to scrape
MAX_INTERVIEWS_PER_PAGE = 20  # Expected interviews per page
DELAY_BETWEEN_PAGES = 3  # Seconds to wait between page loads
DELAY_BETWEEN_REQUESTS = 2  # Seconds to wait between API requests

# ========================
# OUTPUT CONFIGURATION
# ========================

# File paths
OUTPUT_DIR = "output"
DATA_DIR = "data"
LOGS_DIR = "logs"

# File naming
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"
JSON_FILENAME_TEMPLATE = "{company}_interviews_{timestamp}.json"
QUESTIONS_FILENAME_TEMPLATE = "{company}_questions_{timestamp}.txt"

# ========================
# ANALYSIS CONFIGURATION
# ========================

# Question extraction settings
CHUNK_SIZE = 25  # Interviews per chunk for AI processing
MIN_QUESTION_LENGTH = 15  # Minimum characters for a valid question
MAX_QUESTION_LENGTH = 300  # Maximum characters for a valid question

# Question categories
QUESTION_CATEGORIES = [
    "coding_questions",
    "technical_questions", 
    "sql_questions",
    "behavioral_questions",
    "hr_questions",
    "system_design_questions",
    "project_questions"
]

# Keywords for categorization
CODING_KEYWORDS = [
    "algorithm", "data structure", "array", "string", "linked list", 
    "tree", "graph", "dp", "dynamic programming", "recursion", 
    "sorting", "searching", "leetcode", "coding problem", "programming"
]

TECHNICAL_KEYWORDS = [
    "javascript", "python", "java", "sql", "database", "mysql", 
    "mongodb", "react", "node", "express", "aws", "s3", "linux", 
    "security", "json", "oops", "oop", "dbms", "operating system"
]

# ========================
# LOGGING CONFIGURATION
# ========================

LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_logging": True,
    "console_logging": True
}

# ========================
# RATE LIMITING
# ========================

# API rate limits (adjust based on your plan)
GEMINI_RATE_LIMITS = {
    "requests_per_minute": 60,
    "requests_per_day": 1500,  # Free tier limit
    "tokens_per_request": 1048576  # 1M tokens for premium models
}

# Web scraping rate limits
SCRAPING_RATE_LIMITS = {
    "requests_per_minute": 30,
    "delay_between_requests": 2,
    "max_retries": 3,
    "backoff_factor": 1.5
}

# ========================
# QUALITY FILTERS
# ========================

# Filters for question quality
QUALITY_FILTERS = {
    "skip_words": ["lorem", "ipsum", "example", "sample", "test"],
    "min_word_count": 3,
    "max_word_count": 50,
    "require_question_mark": False,
    "remove_duplicates": True
}

# ========================
# COMPANY-SPECIFIC SETTINGS
# ========================

# Company-specific configurations
COMPANY_CONFIGS = {
    "darwinbox": {
        "glassdoor_url": "https://www.glassdoor.co.in/Interview/darwinbox-interview-questions-SRCH_KE0,9.htm",
        "expected_interviews": 200,
        "focus_categories": ["coding_questions", "technical_questions", "behavioral_questions"]
    }
    # Add more companies as needed
}
