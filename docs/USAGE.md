# 📖 Usage Guide

This guide covers how to use the Glassdoor Interview Scraper for different scenarios.

## 🎯 Quick Start

### Basic Scraping

```python
from scrapers.glassdoor_scraper import GlassdoorScraper

# Initialize scraper
scraper = GlassdoorScraper()

# Scrape company interviews
company_url = "https://www.glassdoor.com/Interview/company-interview-questions-SRCH_KE0,7.htm"
results = scraper.scrape_company_interviews(company_url, max_pages=5)

# Save results
scraper.save_results(results, "company_interviews.json")
```

### AI-Powered Analysis

```python
from analyzers.gemini_extractor import GeminiQuestionExtractor
from config import GEMINI_API_KEY

# Initialize AI extractor
extractor = GeminiQuestionExtractor(GEMINI_API_KEY)

# Extract questions
questions, chunks_processed = extractor.extract_questions_from_interviews(results)

# Save extracted questions
extractor.save_results(questions, results['metadata'])
```

## 🏢 Company-Specific Scraping

### Popular Companies

```python
# Tech companies
companies = {
    "google": "https://www.glassdoor.com/Interview/Google-Interview-Questions-E9079.htm",
    "microsoft": "https://www.glassdoor.com/Interview/Microsoft-Interview-Questions-E1651.htm",
    "amazon": "https://www.glassdoor.com/Interview/Amazon-Interview-Questions-E6036.htm",
    "darwinbox": "https://www.glassdoor.co.in/Interview/darwinbox-interview-questions-SRCH_KE0,9.htm"
}

for company, url in companies.items():
    print(f"🏢 Scraping {company}...")
    results = scraper.scrape_company_interviews(url, max_pages=10)
    scraper.save_results(results, f"{company}_interviews.json")
```

### Custom Company URLs

```python
# Find company interview URL on Glassdoor
# Format: https://www.glassdoor.com/Interview/[company-name]-interview-questions-SRCH_KE0,[length].htm

def scrape_custom_company(company_name, glassdoor_url, max_pages=10):
    scraper = GlassdoorScraper({
        'max_pages': max_pages,
        'delay_between_pages': 3,
        'output_dir': f'output/{company_name}'
    })
    
    results = scraper.scrape_company_interviews(glassdoor_url, max_pages)
    filename = f"{company_name}_interviews_{datetime.now().strftime('%Y%m%d')}.json"
    
    return scraper.save_results(results, filename)
```

## 🤖 AI Analysis Options

### Model Selection

```python
# Premium model (best quality, slower)
extractor = GeminiQuestionExtractor(api_key, "gemini-1.5-pro")

# Fast model (good quality, faster)
extractor = GeminiQuestionExtractor(api_key, "gemini-2.0-flash-exp")

# Balanced model
extractor = GeminiQuestionExtractor(api_key, "gemini-1.5-flash")
```

### Processing Options

```python
# Process all interviews
questions, chunks = extractor.extract_questions_from_interviews(
    interview_data,
    chunk_size=25,      # Interviews per API call
    max_chunks=None     # Process all chunks
)

# Process subset for testing
questions, chunks = extractor.extract_questions_from_interviews(
    interview_data,
    chunk_size=10,      # Smaller chunks for better quality
    max_chunks=5        # Only first 5 chunks (50 interviews)
)
```

## 📊 Basic Analysis (No AI Required)

```python
from analyzers.basic_analyzer import BasicInterviewAnalyzer

# Initialize basic analyzer
analyzer = BasicInterviewAnalyzer()

# Analyze interviews
results = analyzer.analyze_interviews(interview_data)

# Save results
analyzer.save_results(results)

# Access specific data
coding_questions = results['questions']['coding_questions']
technical_topics = results['statistics']['top_technical_topics']
study_plan = results['study_plan']
```

## 🎛️ Advanced Configuration

### Custom Browser Settings

```python
from scrapers.glassdoor_scraper import GlassdoorScraper

config = {
    'max_pages': 20,
    'delay_between_pages': 5,
    'headless': True,           # Run in background
    'block_images': True,       # Faster loading
    'output_dir': 'custom_output'
}

scraper = GlassdoorScraper(config)
```

### Rate Limiting

```python
# Conservative settings (slower but safer)
config = {
    'delay_between_pages': 10,
    'delay_between_requests': 5,
    'max_retries': 5
}

# Aggressive settings (faster but may hit limits)
config = {
    'delay_between_pages': 1,
    'delay_between_requests': 0.5,
    'max_retries': 2
}
```

## 📁 Data Management

### File Organization

```
output/
├── company1/
│   ├── interviews_20250803.json
│   ├── questions_20250803.json
│   └── analysis_20250803.txt
├── company2/
│   └── ...
└── combined/
    └── all_companies_analysis.json
```

### Combining Multiple Companies

```python
import json
from datetime import datetime

def combine_company_data(company_files):
    combined_data = {
        'metadata': {
            'combined_date': datetime.now().isoformat(),
            'companies': [],
            'total_interviews': 0
        },
        'interviews': []
    }
    
    for company, filepath in company_files.items():
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Add company info to each interview
        for interview in data['interviews']:
            interview['company'] = company
        
        combined_data['interviews'].extend(data['interviews'])
        combined_data['metadata']['companies'].append(company)
        combined_data['metadata']['total_interviews'] += len(data['interviews'])
    
    return combined_data

# Usage
companies = {
    'google': 'output/google_interviews.json',
    'microsoft': 'output/microsoft_interviews.json',
    'amazon': 'output/amazon_interviews.json'
}

combined = combine_company_data(companies)
```

## 🔍 Question Analysis

### Filter by Category

```python
def filter_questions_by_category(questions, categories):
    filtered = {}
    for category in categories:
        if category in questions:
            filtered[category] = questions[category]
    return filtered

# Get only coding and technical questions
coding_tech = filter_questions_by_category(
    questions, 
    ['coding_questions', 'technical_questions']
)
```

### Search Questions

```python
def search_questions(questions, search_term):
    results = {}
    for category, question_list in questions.items():
        matching = [q for q in question_list if search_term.lower() in q.lower()]
        if matching:
            results[category] = matching
    return results

# Find all questions about JavaScript
js_questions = search_questions(questions, "javascript")
```

### Export to Different Formats

```python
import csv
import pandas as pd

def export_to_csv(questions, filename):
    rows = []
    for category, question_list in questions.items():
        for question in question_list:
            rows.append({'category': category, 'question': question})
    
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)

def export_to_markdown(questions, filename):
    with open(filename, 'w') as f:
        f.write("# Interview Questions\n\n")
        for category, question_list in questions.items():
            f.write(f"## {category.replace('_', ' ').title()}\n\n")
            for i, question in enumerate(question_list, 1):
                f.write(f"{i}. {question}\n")
            f.write("\n")
```

## 🎯 Interview Preparation Workflows

### Complete Preparation Pipeline

```python
def complete_interview_prep(company_url, company_name):
    """Complete interview preparation pipeline"""
    
    # Step 1: Scrape interviews
    print(f"🔍 Step 1: Scraping {company_name} interviews...")
    scraper = GlassdoorScraper()
    interview_data = scraper.scrape_company_interviews(company_url, max_pages=10)
    
    # Step 2: AI extraction
    print("🤖 Step 2: AI question extraction...")
    extractor = GeminiQuestionExtractor(GEMINI_API_KEY)
    questions, chunks = extractor.extract_questions_from_interviews(interview_data)
    
    # Step 3: Basic analysis
    print("📊 Step 3: Statistical analysis...")
    analyzer = BasicInterviewAnalyzer()
    analysis = analyzer.analyze_interviews(interview_data)
    
    # Step 4: Generate study materials
    print("📚 Step 4: Generating study materials...")
    
    # Save all results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{company_name}_{timestamp}"
    
    scraper.save_results(interview_data, f"{base_filename}_raw.json")
    extractor.save_results(questions, interview_data['metadata'])
    analyzer.save_results(analysis)
    
    # Create summary
    summary = {
        'company': company_name,
        'total_interviews': len(interview_data['interviews']),
        'total_questions': sum(len(qs) for qs in questions.values()),
        'top_categories': sorted(questions.items(), key=lambda x: len(x[1]), reverse=True)[:3],
        'study_plan': analysis['study_plan']
    }
    
    print(f"✅ Complete! Found {summary['total_questions']} questions from {summary['total_interviews']} interviews")
    return summary

# Usage
summary = complete_interview_prep(
    "https://www.glassdoor.com/Interview/darwinbox-interview-questions-SRCH_KE0,9.htm",
    "darwinbox"
)
```

### Quick Analysis for Existing Data

```python
def quick_analysis(json_file):
    """Quick analysis of existing interview data"""
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Basic stats
    interviews = data['interviews']
    print(f"📊 Total interviews: {len(interviews)}")
    
    # Difficulty distribution
    difficulties = {}
    for interview in interviews:
        diff = interview.get('difficulty', 'Unknown')
        difficulties[diff] = difficulties.get(diff, 0) + 1
    
    print("📈 Difficulty distribution:")
    for diff, count in sorted(difficulties.items()):
        print(f"   {diff}: {count}")
    
    # Quick question extraction
    analyzer = BasicInterviewAnalyzer()
    results = analyzer.analyze_interviews(data)
    
    print(f"🎯 Extracted {results['metadata']['total_questions_extracted']} questions")
    for category, questions in results['questions'].items():
        if questions:
            print(f"   {category}: {len(questions)} questions")

# Usage
quick_analysis("output/company_interviews.json")
```

## 🚨 Error Handling

### Common Issues and Solutions

```python
def robust_scraping(company_url, max_retries=3):
    """Robust scraping with error handling"""
    
    for attempt in range(max_retries):
        try:
            scraper = GlassdoorScraper({
                'delay_between_pages': 5,  # Longer delays
                'headless': True           # Avoid detection
            })
            
            results = scraper.scrape_company_interviews(company_url, max_pages=5)
            return results
            
        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"🔄 Retrying in 10 seconds...")
                time.sleep(10)
            else:
                print("💥 All attempts failed!")
                raise

def safe_ai_extraction(interview_data, max_retries=3):
    """Safe AI extraction with fallback"""
    
    try:
        # Try AI extraction first
        extractor = GeminiQuestionExtractor(GEMINI_API_KEY)
        questions, chunks = extractor.extract_questions_from_interviews(interview_data)
        print(f"✅ AI extraction successful: {sum(len(qs) for qs in questions.values())} questions")
        return questions
        
    except Exception as e:
        print(f"❌ AI extraction failed: {str(e)}")
        print("🔄 Falling back to basic analysis...")
        
        # Fallback to basic analysis
        analyzer = BasicInterviewAnalyzer()
        results = analyzer.analyze_interviews(interview_data)
        return results['questions']
```

## 📈 Performance Tips

### Optimize for Speed

```python
# Fast scraping configuration
fast_config = {
    'headless': True,
    'block_images': True,
    'delay_between_pages': 1,
    'max_pages': 5
}

# Large chunk processing for AI
large_chunks = {
    'chunk_size': 50,
    'max_chunks': None
}
```

### Optimize for Quality

```python
# Quality scraping configuration
quality_config = {
    'headless': False,
    'delay_between_pages': 5,
    'max_pages': 20
}

# Small chunk processing for AI
small_chunks = {
    'chunk_size': 10,
    'max_chunks': None
}
```

## 🎉 Success Stories

### Real Usage Examples

```python
# Example 1: Comprehensive FAANG preparation
faang_companies = {
    'google': 'https://www.glassdoor.com/Interview/Google-Interview-Questions-E9079.htm',
    'facebook': 'https://www.glassdoor.com/Interview/Meta-Interview-Questions-E40772.htm',
    'amazon': 'https://www.glassdoor.com/Interview/Amazon-Interview-Questions-E6036.htm',
    'netflix': 'https://www.glassdoor.com/Interview/Netflix-Interview-Questions-E11891.htm',
    'apple': 'https://www.glassdoor.com/Interview/Apple-Interview-Questions-E1138.htm'
}

all_questions = {}
for company, url in faang_companies.items():
    print(f"Processing {company}...")
    data = scraper.scrape_company_interviews(url, max_pages=10)
    questions, _ = extractor.extract_questions_from_interviews(data)
    all_questions[company] = questions

# Combine and analyze
combined_questions = combine_questions(all_questions)
print(f"Total questions across FAANG: {sum(len(qs) for qs in combined_questions.values())}")
```

This usage guide should help you get the most out of the scraper! 🚀
