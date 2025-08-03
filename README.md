# 🎯 Glassdoor Interview Scraper & AI Analyzer

A comprehensive web scraping and AI-powered analysis tool for extracting and categorizing interview questions from Glassdoor. Built for interview preparation with advanced question extraction using Google's Gemini AI.

## 🚀 Features

- **Web Scraping**: Automated Glassdoor interview review extraction with pagination
- **AI-Powered Analysis**: Advanced question extraction using Gemini 2.0 Flash Exp
- **Smart Categorization**: Automatically categorizes questions into 7 types
- **Comprehensive Coverage**: Processes all interview reviews for complete preparation
- **Export Options**: JSON and human-readable text formats

## 📊 Results Achieved

- ✅ **197 interview reviews** scraped successfully
- ✅ **154 premium questions** extracted using AI
- ✅ **7 question categories** for focused study
- ✅ **52 coding questions** with specific algorithms
- ✅ **29 technical questions** covering various technologies
- ✅ **12 SQL questions** for database preparation

## 🛠️ Tech Stack

- **Python 3.12+**
- **Botasaurus** - Human-like browser automation
- **Google Generative AI** - Advanced question extraction
- **Selenium** - Web driver automation
- **BeautifulSoup4** - HTML parsing
- **JSON** - Data storage and export

## 📁 Project Structure

```
glassdoor-interview-scraper/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── config.py                          # Configuration settings
├── scrapers/
│   ├── glassdoor_scraper.py          # Main scraper implementation
│   └── scraper_utils.py              # Utility functions
├── analyzers/
│   ├── gemini_extractor.py           # AI-powered question extraction
│   ├── basic_analyzer.py             # Regex-based analysis
│   └── analyzer_utils.py             # Analysis utilities
├── data/
│   └── sample_output.json            # Sample scraped data
├── docs/
│   ├── SETUP.md                      # Detailed setup instructions
│   ├── USAGE.md                      # Usage examples and guides
│   └── METHODOLOGY.md                # Technical approach and decisions
└── examples/
    ├── basic_scraping.py             # Simple scraping example
    └── ai_extraction.py              # AI extraction example
```

## 🚀 Quick Start

### 1. Installation

```bash
git clone https://github.com/yourusername/glassdoor-interview-scraper.git
cd glassdoor-interview-scraper
pip install -r requirements.txt
```

### 2. Configuration

```bash
cp config.py.example config.py
# Edit config.py with your settings
```

### 3. Basic Scraping

```python
from scrapers.glassdoor_scraper import scrape_company_interviews

# Scrape interview data
results = scrape_company_interviews(
    company_name="YourCompany",
    max_pages=10
)
```

### 4. AI-Powered Analysis

```python
from analyzers.gemini_extractor import extract_questions_with_ai

# Extract questions using AI
questions = extract_questions_with_ai(
    interview_data=results,
    api_key="your-gemini-api-key"
)
```

## 📋 Question Categories

The AI analyzer categorizes questions into:

- 💻 **Coding Questions** (52) - Algorithms, data structures, programming challenges
- 🛠️ **Technical Questions** (29) - Technology-specific questions
- 🗄️ **SQL Questions** (12) - Database queries and concepts
- 🗣️ **Behavioral Questions** (25) - Soft skills and experience
- 👔 **HR Questions** (8) - Company and role-specific
- 🏗️ **System Design Questions** (1) - Architecture and scalability
- 📋 **Project Questions** (27) - Previous work experience

## 🔧 Advanced Features

### Premium AI Models
- **Gemini 2.0 Flash Exp** - Latest and most advanced
- **Gemini 1.5 Pro** - High accuracy for complex analysis
- **Gemini 1.5 Flash** - Fast processing for large datasets

### Smart Processing
- **Large Chunk Processing** - 5x more efficient than basic extraction
- **Advanced Deduplication** - Quality filtering and duplicate removal
- **Context Preservation** - Maintains interview context for better extraction

### Export Formats
- **JSON** - Structured data for further processing
- **Text** - Human-readable format for study
- **Categorized Lists** - Organized by question type

## 📊 Performance Metrics

| Metric | Basic Extraction | Premium AI Extraction |
|--------|------------------|----------------------|
| Questions Extracted | 118 | 154 |
| Processing Chunks | 40 small | 8 large |
| Processing Time | ~3 minutes | ~1 minute |
| Categories | 5 | 7 |
| Accuracy | Good | Excellent |

## 🔒 Privacy & Ethics

- **Rate Limiting** - Respects website rate limits
- **User-Agent Rotation** - Mimics human browsing behavior
- **Cookie Handling** - Proper session management
- **Data Privacy** - No personal information stored
- **Ethical Scraping** - Follows robots.txt and ToS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect Glassdoor's Terms of Service and use responsibly. Always check robots.txt and rate limits before scraping.

## 🙏 Acknowledgments

- **Botasaurus** - For excellent browser automation framework
- **Google Generative AI** - For powerful question extraction capabilities
- **Glassdoor** - For providing valuable interview insights

## 📞 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/)
2. Search existing [issues](https://github.com/yourusername/glassdoor-interview-scraper/issues)
3. Create a new issue with detailed information

---

**Happy Interview Preparation!** 🎯🚀
