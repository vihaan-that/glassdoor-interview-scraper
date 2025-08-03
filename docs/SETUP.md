# 🛠️ Setup Guide

This guide will help you set up the Glassdoor Interview Scraper on your system.

## 📋 Prerequisites

- **Python 3.8+** (Recommended: Python 3.12)
- **Git** for cloning the repository
- **Chrome/Chromium browser** (for Selenium WebDriver)
- **Google Generative AI API key** (for AI-powered extraction)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/glassdoor-interview-scraper.git
cd glassdoor-interview-scraper
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Linux/Mac:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

#### Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

#### Update Configuration

```bash
# Copy the config template
cp config.py config.py.local

# Edit the configuration file
nano config.py  # or use your preferred editor
```

Update the following in `config.py`:

```python
# Replace with your actual API key
GEMINI_API_KEY = "your-actual-api-key-here"

# Choose your preferred model
GEMINI_MODEL = "gemini-2.0-flash-exp"  # or "gemini-1.5-pro"
```

### 5. Create Output Directories

```bash
mkdir -p output data logs
```

## 🧪 Test Installation

### Basic Test

```python
# test_installation.py
from scrapers.glassdoor_scraper import GlassdoorScraper
from analyzers.basic_analyzer import BasicInterviewAnalyzer

print("✅ All imports successful!")
print("🎯 Installation complete!")
```

```bash
python test_installation.py
```

### Test Gemini API

```python
# test_gemini.py
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello, world!")
print("✅ Gemini API working!")
print(f"Response: {response.text}")
```

```bash
python test_gemini.py
```

## ⚙️ Configuration Options

### Browser Settings

```python
BROWSER_CONFIG = {
    "headless": False,        # Set to True for headless mode
    "block_images": True,     # Block images for faster loading
    "window_size": (1920, 1080)
}
```

### Scraping Limits

```python
MAX_PAGES = 10                    # Maximum pages to scrape
DELAY_BETWEEN_PAGES = 3          # Seconds between page loads
DELAY_BETWEEN_REQUESTS = 2       # Seconds between API requests
```

### AI Model Selection

Available models (in order of recommendation):

1. **`gemini-2.0-flash-exp`** - Latest, fastest, largest context
2. **`gemini-1.5-pro`** - High accuracy, good for complex analysis
3. **`gemini-1.5-flash`** - Fast, good balance of speed and quality

## 🔧 Troubleshooting

### Common Issues

#### 1. Chrome Driver Issues

```bash
# Install Chrome/Chromium
sudo apt update
sudo apt install chromium-browser  # Linux
# or download Chrome from official website

# Update webdriver-manager
pip install --upgrade webdriver-manager
```

#### 2. API Key Issues

```bash
# Verify API key format
echo $GEMINI_API_KEY | wc -c  # Should be around 39 characters
```

#### 3. Permission Issues

```bash
# Fix directory permissions
chmod -R 755 glassdoor-interview-scraper/
```

#### 4. Import Errors

```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Debug Mode

Enable debug logging in `config.py`:

```python
LOGGING_CONFIG = {
    "level": "DEBUG",
    "console_logging": True,
    "file_logging": True
}
```

### Rate Limiting Issues

If you encounter rate limiting:

1. **Increase delays** in configuration
2. **Reduce chunk size** for AI processing
3. **Check API quotas** in Google AI Studio

## 🔒 Security Best Practices

### API Key Security

1. **Never commit API keys** to version control
2. **Use environment variables** for production
3. **Rotate keys regularly**

```bash
# Use environment variables
export GEMINI_API_KEY="your-key-here"
```

### Ethical Scraping

1. **Respect robots.txt**
2. **Use appropriate delays**
3. **Don't overload servers**
4. **Follow Terms of Service**

## 📊 Performance Optimization

### For Large Datasets

```python
# Increase chunk size for AI processing
CHUNK_SIZE = 50  # Process more interviews per API call

# Use headless mode for faster scraping
BROWSER_CONFIG["headless"] = True

# Enable image blocking
BROWSER_CONFIG["block_images"] = True
```

### For Better Quality

```python
# Use premium AI model
GEMINI_MODEL = "gemini-1.5-pro"

# Reduce chunk size for better context
CHUNK_SIZE = 10

# Enable detailed logging
LOGGING_CONFIG["level"] = "DEBUG"
```

## 🆘 Getting Help

### Check Logs

```bash
# View recent logs
tail -f logs/scraper.log

# Search for errors
grep -i error logs/*.log
```

### Common Commands

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Clean cache
pip cache purge

# Reinstall from scratch
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Support Resources

1. **Documentation**: Check `docs/` folder
2. **Examples**: See `examples/` folder
3. **Issues**: Create GitHub issue with logs
4. **API Documentation**: [Google AI Studio Docs](https://ai.google.dev/docs)

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed successfully
- [ ] Gemini API key configured
- [ ] Output directories created
- [ ] Basic test passes
- [ ] Gemini API test passes
- [ ] Chrome/Chromium browser available

Once all items are checked, you're ready to start scraping! 🎉

## 🚀 Next Steps

1. Read the [Usage Guide](USAGE.md)
2. Check out [Examples](../examples/)
3. Review the [Methodology](METHODOLOGY.md)
4. Start with a small test scrape
