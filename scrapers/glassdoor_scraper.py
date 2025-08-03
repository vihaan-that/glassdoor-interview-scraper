"""
Glassdoor Interview Scraper
===========================

A robust web scraper for extracting interview reviews from Glassdoor using Botasaurus.
Handles pagination, login walls, and cookie consent automatically.

Author: Interview Preparation Assistant
License: MIT
"""

import json
import time
from datetime import datetime
from typing import List, Dict, Optional
from botasaurus.browser import browser, Driver
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GlassdoorScraper:
    """
    Main scraper class for Glassdoor interview reviews
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the scraper with configuration
        
        Args:
            config: Dictionary containing scraper configuration
        """
        self.config = config or self._default_config()
        self.interviews = []
        self.stats = {
            'pages_processed': 0,
            'interviews_found': 0,
            'errors': 0,
            'start_time': None,
            'end_time': None
        }
    
    def _default_config(self) -> Dict:
        """Default configuration if none provided"""
        return {
            'max_pages': 10,
            'delay_between_pages': 3,
            'headless': False,
            'block_images': True,
            'output_dir': 'output'
        }
    
    @browser(
        block_images=True,
        headless=False,
        add_arguments=[
            "--disable-geolocation",
            "--disable-permissions-api", 
            "--disable-web-security",
            "--disable-notifications",
            "--disable-popup-blocking"
        ]
    )
    def scrape_company_interviews(self, driver: Driver, company_url: str, 
                                max_pages: int = 10) -> Dict:
        """
        Scrape interview reviews for a specific company
        
        Args:
            driver: Botasaurus browser driver
            company_url: Glassdoor URL for company interviews
            max_pages: Maximum number of pages to scrape
            
        Returns:
            Dictionary containing scraped interview data and metadata
        """
        logger.info(f"🚀 Starting Glassdoor scraping for: {company_url}")
        self.stats['start_time'] = datetime.now()
        
        try:
            # Navigate to the company interview page
            driver.get(company_url)
            driver.sleep(3)
            
            # Handle cookie consent and login walls
            self._handle_popups(driver)
            
            # Extract interviews from all pages
            page_num = 1
            while page_num <= max_pages:
                logger.info(f"📄 Processing page {page_num}/{max_pages}")
                
                # Extract interviews from current page
                page_interviews = self._extract_page_interviews(driver, page_num)
                self.interviews.extend(page_interviews)
                
                self.stats['pages_processed'] = page_num
                self.stats['interviews_found'] = len(self.interviews)
                
                logger.info(f"✅ Page {page_num}: Found {len(page_interviews)} interviews "
                           f"(Total: {len(self.interviews)})")
                
                # Try to navigate to next page
                if not self._navigate_to_next_page(driver, page_num):
                    logger.info("🏁 No more pages available")
                    break
                    
                page_num += 1
                driver.sleep(self.config['delay_between_pages'])
            
            # Finalize results
            self.stats['end_time'] = datetime.now()
            duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
            
            results = {
                'metadata': {
                    'company_url': company_url,
                    'scraping_date': self.stats['start_time'].isoformat(),
                    'duration_seconds': duration,
                    'pages_processed': self.stats['pages_processed'],
                    'total_interviews': len(self.interviews)
                },
                'interviews': self.interviews,
                'stats': self.stats
            }
            
            logger.info(f"🎉 Scraping complete! Found {len(self.interviews)} interviews "
                       f"in {duration:.1f} seconds")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Scraping failed: {str(e)}")
            self.stats['errors'] += 1
            raise
    
    def _handle_popups(self, driver: Driver):
        """Handle cookie consent and login popups"""
        try:
            # Cookie consent
            cookie_buttons = driver.select_all("button[data-test='gdpr-consent-accept']")
            if cookie_buttons:
                cookie_buttons[0].click()
                driver.sleep(2)
                logger.info("✅ Accepted cookie consent")
            
            # Login wall dismiss
            close_buttons = driver.select_all("button[data-test='close-x']")
            if close_buttons:
                close_buttons[0].click()
                driver.sleep(2)
                logger.info("✅ Dismissed login popup")
                
        except Exception as e:
            logger.warning(f"⚠️ Popup handling warning: {str(e)}")
    
    def _extract_page_interviews(self, driver: Driver, page_num: int) -> List[Dict]:
        """Extract interview data from current page"""
        interviews = []
        
        try:
            # Wait for content to load
            driver.sleep(2)
            
            # Find interview containers
            interview_elements = driver.select_all("div[data-test='InterviewReview']")
            
            if not interview_elements:
                # Try alternative selector
                interview_elements = driver.select_all(".interview-item")
            
            logger.info(f"📋 Found {len(interview_elements)} interview elements on page {page_num}")
            
            for idx, element in enumerate(interview_elements):
                try:
                    interview_data = self._extract_interview_data(element, page_num, idx + 1)
                    if interview_data:
                        interviews.append(interview_data)
                        
                except Exception as e:
                    logger.warning(f"⚠️ Failed to extract interview {idx + 1}: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"❌ Page extraction failed: {str(e)}")
            
        return interviews
    
    def _extract_interview_data(self, element, page_num: int, interview_num: int) -> Optional[Dict]:
        """Extract data from a single interview element"""
        try:
            # Extract interview text content
            text_elements = element.select_all("p.truncated-text_truncate__021Uu.interview-details_textStyle__gmhSJ")
            raw_text = " ".join([elem.text.strip() for elem in text_elements if elem.text.strip()])
            
            if not raw_text or len(raw_text) < 50:
                return None
            
            # Extract metadata
            position = "Software Developer"  # Default
            experience = "Not specified"
            difficulty = "Not specified"
            outcome = "Not specified"
            
            # Try to extract position
            try:
                position_elem = element.select("span[data-test='position']")
                if position_elem:
                    position = position_elem.text.strip()
            except:
                pass
            
            # Try to extract experience
            try:
                exp_elem = element.select("span[data-test='experience']")
                if exp_elem:
                    experience = exp_elem.text.strip()
            except:
                pass
            
            # Try to extract difficulty
            try:
                diff_elem = element.select("span[data-test='difficulty']")
                if diff_elem:
                    difficulty = diff_elem.text.strip()
            except:
                pass
            
            # Try to extract outcome
            try:
                outcome_elem = element.select("span[data-test='outcome']")
                if outcome_elem:
                    outcome = outcome_elem.text.strip()
            except:
                pass
            
            return {
                'id': f"page_{page_num}_interview_{interview_num}",
                'page_number': page_num,
                'position': position,
                'experience': experience,
                'difficulty': difficulty,
                'outcome': outcome,
                'raw_text': raw_text,
                'text_length': len(raw_text),
                'extracted_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.warning(f"⚠️ Interview data extraction failed: {str(e)}")
            return None
    
    def _navigate_to_next_page(self, driver: Driver, current_page: int) -> bool:
        """Navigate to the next page of results"""
        try:
            # Look for pagination buttons
            next_buttons = driver.select_all("a.pagination_ListItemButton__se7rv")
            
            for button in next_buttons:
                button_text = button.text.strip()
                if button_text.isdigit() and int(button_text) == current_page + 1:
                    logger.info(f"🔄 Navigating to page {current_page + 1}")
                    button.click()
                    driver.sleep(3)
                    return True
            
            # Try next arrow button
            next_arrow = driver.select_all("button[aria-label='Next']")
            if next_arrow:
                next_arrow[0].click()
                driver.sleep(3)
                return True
                
            return False
            
        except Exception as e:
            logger.warning(f"⚠️ Navigation failed: {str(e)}")
            return False
    
    def save_results(self, results: Dict, filename: str = None):
        """Save scraping results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"interviews_{timestamp}.json"
        
        filepath = f"{self.config['output_dir']}/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Results saved to: {filepath}")
        return filepath


def main():
    """Example usage of the scraper"""
    # Configuration
    config = {
        'max_pages': 10,
        'delay_between_pages': 3,
        'headless': False,
        'output_dir': 'output'
    }
    
    # Initialize scraper
    scraper = GlassdoorScraper(config)
    
    # Scrape Darwinbox interviews (example)
    company_url = "https://www.glassdoor.co.in/Interview/darwinbox-interview-questions-SRCH_KE0,9.htm"
    
    try:
        results = scraper.scrape_company_interviews(company_url, max_pages=10)
        scraper.save_results(results)
        
        print(f"✅ Successfully scraped {results['metadata']['total_interviews']} interviews!")
        
    except Exception as e:
        print(f"❌ Scraping failed: {str(e)}")


if __name__ == "__main__":
    main()
