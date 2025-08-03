#!/usr/bin/env python3
"""
Basic Scraping Example
======================

Simple example showing how to scrape interview data from Glassdoor.
This example demonstrates the core functionality without AI analysis.

Usage:
    python examples/basic_scraping.py
"""

import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.glassdoor_scraper import GlassdoorScraper
from analyzers.basic_analyzer import BasicInterviewAnalyzer


def basic_scraping_example():
    """
    Basic scraping example for beginners
    """
    print("🚀 Basic Glassdoor Scraping Example")
    print("=" * 40)
    
    # Configuration
    config = {
        'max_pages': 3,              # Start small for testing
        'delay_between_pages': 5,    # Conservative delay
        'headless': False,           # See what's happening
        'output_dir': 'output'
    }
    
    # Company to scrape (example)
    company_name = "darwinbox"
    company_url = "https://www.glassdoor.co.in/Interview/darwinbox-interview-questions-SRCH_KE0,9.htm"
    
    try:
        # Step 1: Initialize scraper
        print(f"🔧 Initializing scraper for {company_name}...")
        scraper = GlassdoorScraper(config)
        
        # Step 2: Scrape interview data
        print(f"🕷️ Scraping interviews from {company_url}...")
        print("   This may take a few minutes...")
        
        results = scraper.scrape_company_interviews(company_url, max_pages=config['max_pages'])
        
        # Step 3: Save raw results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_filename = f"{company_name}_raw_{timestamp}.json"
        scraper.save_results(results, raw_filename)
        
        # Step 4: Basic analysis
        print("📊 Performing basic analysis...")
        analyzer = BasicInterviewAnalyzer()
        analysis = analyzer.analyze_interviews(results)
        
        # Step 5: Save analysis results
        analysis_filename = f"{company_name}_analysis_{timestamp}"
        analyzer.save_results(analysis, "output")
        
        # Step 6: Print summary
        print("\n✅ SCRAPING COMPLETE!")
        print("=" * 30)
        print(f"🏢 Company: {company_name}")
        print(f"📊 Interviews found: {results['metadata']['total_interviews']}")
        print(f"📄 Pages processed: {results['metadata']['pages_processed']}")
        print(f"⏱️ Duration: {results['metadata']['duration_seconds']:.1f} seconds")
        
        # Analysis summary
        total_questions = analysis['metadata']['total_questions_extracted']
        print(f"🎯 Questions extracted: {total_questions}")
        
        print(f"\n📁 Files created:")
        print(f"   • output/{raw_filename}")
        print(f"   • output/{analysis_filename}.json")
        print(f"   • output/{analysis_filename}.txt")
        
        # Top categories
        print(f"\n🏆 Top question categories:")
        questions = analysis['questions']
        sorted_categories = sorted(questions.items(), key=lambda x: len(x[1]), reverse=True)
        
        for category, question_list in sorted_categories[:3]:
            if question_list:
                category_name = category.replace('_', ' ').title()
                print(f"   • {category_name}: {len(question_list)} questions")
        
        print(f"\n🎉 Success! Check the output files for detailed results.")
        
        return results, analysis
        
    except Exception as e:
        print(f"❌ Scraping failed: {str(e)}")
        print(f"💡 Try reducing max_pages or increasing delays")
        return None, None


def quick_analysis_example():
    """
    Example of analyzing existing data
    """
    print("\n🔍 Quick Analysis Example")
    print("=" * 30)
    
    # Look for existing data files
    data_files = []
    if os.path.exists('output'):
        for filename in os.listdir('output'):
            if filename.endswith('_raw.json'):
                data_files.append(f"output/{filename}")
    
    if not data_files:
        print("❌ No existing data files found. Run scraping first.")
        return
    
    # Use the most recent file
    latest_file = max(data_files, key=os.path.getmtime)
    print(f"📂 Analyzing: {latest_file}")
    
    try:
        # Load data
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Quick stats
        interviews = data['interviews']
        print(f"📊 Total interviews: {len(interviews)}")
        
        # Difficulty distribution
        difficulties = {}
        for interview in interviews:
            diff = interview.get('difficulty', 'Unknown')
            difficulties[diff] = difficulties.get(diff, 0) + 1
        
        print("📈 Difficulty distribution:")
        for diff, count in sorted(difficulties.items()):
            print(f"   {diff}: {count} interviews")
        
        # Analyze with basic analyzer
        analyzer = BasicInterviewAnalyzer()
        results = analyzer.analyze_interviews(data)
        
        print(f"🎯 Questions extracted: {results['metadata']['total_questions_extracted']}")
        
        # Top technical topics
        top_topics = results['statistics']['top_technical_topics']
        print("🔥 Top technical topics:")
        for topic, count in list(top_topics.items())[:5]:
            print(f"   {topic}: {count} mentions")
            
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")


def main():
    """
    Main function demonstrating basic usage
    """
    print("🎯 Glassdoor Interview Scraper - Basic Examples")
    print("=" * 50)
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Example 1: Basic scraping
    print("Example 1: Basic Scraping")
    results, analysis = basic_scraping_example()
    
    if results:
        # Example 2: Quick analysis of existing data
        print("\n" + "=" * 50)
        print("Example 2: Quick Analysis")
        quick_analysis_example()
    
    print("\n🎉 Examples complete!")
    print("💡 Next steps:")
    print("   • Try the AI extraction example")
    print("   • Experiment with different companies")
    print("   • Adjust configuration for your needs")


if __name__ == "__main__":
    main()
