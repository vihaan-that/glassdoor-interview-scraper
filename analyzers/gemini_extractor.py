"""
Gemini AI Question Extractor
============================

Advanced AI-powered question extraction using Google's Gemini models.
Processes interview data and categorizes questions with high accuracy.

Author: Interview Preparation Assistant
License: MIT
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeminiQuestionExtractor:
    """
    AI-powered question extractor using Google Gemini models
    """
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the Gemini API client
        
        Args:
            api_key: Google Generative AI API key
            model_name: Gemini model to use for extraction
        """
        if api_key == "your-gemini-api-key-here":
            raise ValueError("Please set your actual Gemini API key in config.py")
            
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.model_name = model_name
        
        logger.info(f"🤖 Initialized Gemini extractor with model: {model_name}")
    
    def extract_questions_from_interviews(self, interview_data: Dict, 
                                        chunk_size: int = 25,
                                        max_chunks: Optional[int] = None) -> Tuple[Dict, int]:
        """
        Extract categorized questions from interview data using AI
        
        Args:
            interview_data: Dictionary containing interview reviews
            chunk_size: Number of interviews to process per API call
            max_chunks: Maximum number of chunks to process (None for all)
            
        Returns:
            Tuple of (extracted_questions_dict, chunks_processed)
        """
        interviews = interview_data.get('interviews', [])
        if not interviews:
            raise ValueError("No interviews found in data")
        
        logger.info(f"📊 Processing {len(interviews)} interviews...")
        
        # Calculate chunks
        total_chunks = (len(interviews) + chunk_size - 1) // chunk_size
        if max_chunks:
            total_chunks = min(total_chunks, max_chunks)
        
        logger.info(f"🎯 Using {total_chunks} chunks of {chunk_size} interviews each")
        
        # Initialize results
        all_questions = {
            "coding_questions": [],
            "technical_questions": [],
            "sql_questions": [],
            "behavioral_questions": [],
            "hr_questions": [],
            "system_design_questions": [],
            "project_questions": []
        }
        
        # Process interviews in chunks
        processed_chunks = 0
        for chunk_num in range(total_chunks):
            start_idx = chunk_num * chunk_size
            end_idx = min(start_idx + chunk_size, len(interviews))
            chunk = interviews[start_idx:end_idx]
            
            logger.info(f"🔄 Processing chunk {chunk_num + 1}/{total_chunks} "
                       f"(interviews {start_idx + 1}-{end_idx})...")
            
            try:
                chunk_questions = self._process_chunk(chunk, chunk_num + 1)
                
                # Merge results
                for category in all_questions:
                    if category in chunk_questions and isinstance(chunk_questions[category], list):
                        all_questions[category].extend(chunk_questions[category])
                
                processed_chunks += 1
                questions_found = sum(len(v) for v in chunk_questions.values() if isinstance(v, list))
                categories_found = len([k for k, v in chunk_questions.items() if v])
                
                logger.info(f"✅ Chunk {chunk_num + 1}: Found {questions_found} questions "
                           f"in {categories_found} categories")
                
            except Exception as e:
                logger.error(f"❌ Error processing chunk {chunk_num + 1}: {str(e)}")
                continue
            
            # Rate limiting
            time.sleep(1)
        
        # Clean and deduplicate
        logger.info("🔧 Cleaning and deduplicating questions...")
        all_questions = self._clean_and_deduplicate(all_questions)
        
        return all_questions, processed_chunks
    
    def _process_chunk(self, interviews: List[Dict], chunk_num: int) -> Dict:
        """Process a single chunk of interviews"""
        # Combine interviews into text
        chunk_text = self._prepare_chunk_text(interviews, chunk_num)
        
        # Create extraction prompt
        prompt = self._create_extraction_prompt(chunk_text)
        
        # Get AI response
        response = self.model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Parse JSON response
        return self._parse_ai_response(response_text)
    
    def _prepare_chunk_text(self, interviews: List[Dict], chunk_num: int) -> str:
        """Prepare interview text for AI processing"""
        chunk_text = f"=== CHUNK {chunk_num} INTERVIEWS ===\n\n"
        
        for i, interview in enumerate(interviews):
            chunk_text += f"--- INTERVIEW {i + 1} ---\n"
            chunk_text += f"Position: {interview.get('position', 'N/A')}\n"
            chunk_text += f"Experience: {interview.get('experience', 'N/A')}\n"
            chunk_text += f"Difficulty: {interview.get('difficulty', 'N/A')}\n"
            chunk_text += f"Outcome: {interview.get('outcome', 'N/A')}\n"
            chunk_text += f"Content: {interview.get('raw_text', '')}\n\n"
        
        return chunk_text
    
    def _create_extraction_prompt(self, chunk_text: str) -> str:
        """Create the AI extraction prompt"""
        return f"""
        You are an expert interview analyst. Extract specific, actionable interview questions from these interview reviews.

        INTERVIEW DATA:
        {chunk_text}

        EXTRACTION REQUIREMENTS:
        1. Extract ONLY actual questions that were asked during interviews
        2. Focus on specific, actionable questions candidates can prepare for
        3. Categorize questions accurately
        4. Include context when helpful (e.g., "for 2+ years experience")
        5. Avoid generic statements - focus on concrete questions

        CATEGORIES:
        - CODING_QUESTIONS: Programming problems, algorithms, data structures, coding challenges
        - TECHNICAL_QUESTIONS: Technology-specific questions (JavaScript, frameworks, databases, etc.)
        - SQL_QUESTIONS: Database queries, SQL-specific problems
        - BEHAVIORAL_QUESTIONS: Personal experience, soft skills, situational questions
        - HR_QUESTIONS: Company-specific, salary, notice period, career goals
        - SYSTEM_DESIGN_QUESTIONS: Architecture, scalability, design problems
        - PROJECT_QUESTIONS: Questions about previous projects, technical decisions

        Return as JSON:
        {{
            "coding_questions": [
                "Implement binary search algorithm",
                "Solve two-sum problem with optimal complexity"
            ],
            "technical_questions": [
                "Explain JavaScript closures with examples",
                "Difference between SQL and NoSQL databases"
            ],
            "sql_questions": [
                "Write a query to find second highest salary",
                "Explain different types of JOINs"
            ],
            "behavioral_questions": [
                "Tell me about a challenging project you worked on",
                "How do you handle conflicts in a team?"
            ],
            "hr_questions": [
                "Why do you want to join this company?",
                "What are your salary expectations?"
            ],
            "system_design_questions": [
                "Design a scalable chat application",
                "How would you handle high traffic loads?"
            ],
            "project_questions": [
                "Explain the architecture of your last project",
                "What challenges did you face and how did you solve them?"
            ]
        }}

        IMPORTANT: 
        - Only include clear, specific questions
        - Ensure questions are interview-ready and actionable
        - Focus on quality over quantity
        - Include variations of similar questions if they add value
        """
    
    def _parse_ai_response(self, response_text: str) -> Dict:
        """Parse AI response and extract JSON"""
        try:
            # Clean JSON response
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text.strip())
            
        except json.JSONDecodeError as e:
            logger.warning(f"⚠️ JSON parsing failed: {str(e)}")
            return {}
    
    def _clean_and_deduplicate(self, all_questions: Dict) -> Dict:
        """Clean and deduplicate extracted questions"""
        for category in all_questions:
            seen = set()
            unique_questions = []
            
            for q in all_questions[category]:
                if isinstance(q, str) and q.strip():
                    q_clean = q.strip()
                    q_lower = q_clean.lower()
                    
                    # Quality filters
                    if (len(q_clean) < 15 or len(q_clean) > 300 or 
                        q_lower in seen or
                        any(skip_word in q_lower for skip_word in ['lorem', 'ipsum', 'example', 'sample'])):
                        continue
                    
                    seen.add(q_lower)
                    unique_questions.append(q_clean)
            
            all_questions[category] = unique_questions
        
        return all_questions
    
    def save_results(self, questions: Dict, metadata: Dict, output_dir: str = "output"):
        """Save extraction results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_filename = f"{output_dir}/questions_{timestamp}.json"
        json_data = {
            "metadata": {
                **metadata,
                "extraction_date": datetime.now().isoformat(),
                "model_used": self.model_name,
                "total_questions": sum(len(questions[cat]) for cat in questions)
            },
            "questions": questions
        }
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        # Save as readable text
        txt_filename = f"{output_dir}/questions_{timestamp}.txt"
        self._save_readable_format(questions, metadata, txt_filename)
        
        logger.info(f"💾 Results saved to:")
        logger.info(f"   • {json_filename}")
        logger.info(f"   • {txt_filename}")
        
        return json_filename, txt_filename
    
    def _save_readable_format(self, questions: Dict, metadata: Dict, filename: str):
        """Save questions in human-readable format"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("🚀 AI-EXTRACTED INTERVIEW QUESTIONS\n")
            f.write("=" * 50 + "\n")
            f.write(f"🤖 Extracted using: {self.model_name}\n")
            f.write(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"📊 Total interviews processed: {metadata.get('total_interviews', 'N/A')}\n\n")
            
            # Categories with emojis
            categories = [
                ("💻 CODING & ALGORITHM QUESTIONS", "coding_questions", "🔥"),
                ("🛠️ TECHNICAL QUESTIONS", "technical_questions", "⚡"),
                ("🗄️ SQL & DATABASE QUESTIONS", "sql_questions", "💾"),
                ("🗣️ BEHAVIORAL QUESTIONS", "behavioral_questions", "🎯"),
                ("👔 HR & COMPANY QUESTIONS", "hr_questions", "🏢"),
                ("🏗️ SYSTEM DESIGN QUESTIONS", "system_design_questions", "🚀"),
                ("📋 PROJECT EXPERIENCE QUESTIONS", "project_questions", "🛠️")
            ]
            
            for title, key, emoji in categories:
                question_list = questions.get(key, [])
                if not question_list:
                    continue
                    
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n")
                
                for i, q in enumerate(question_list, 1):
                    f.write(f"{i:2d}. {emoji} {q}\n")
                f.write(f"\n📊 Total: {len(question_list)} questions\n\n")
            
            # Summary
            total_questions = sum(len(questions[cat]) for cat in questions)
            f.write("📊 EXTRACTION SUMMARY\n")
            f.write("=" * 25 + "\n")
            f.write(f"🎯 Total Questions: {total_questions}\n")
            for title, key, emoji in categories:
                if questions.get(key):
                    f.write(f"   {emoji} {title.split()[1]} Questions: {len(questions[key])}\n")


def main():
    """Example usage of the extractor"""
    # This would normally be imported from config
    API_KEY = "your-gemini-api-key-here"  # Replace with actual key
    
    if API_KEY == "your-gemini-api-key-here":
        print("❌ Please set your Gemini API key in config.py")
        return
    
    # Initialize extractor
    extractor = GeminiQuestionExtractor(API_KEY, "gemini-2.0-flash-exp")
    
    # Load interview data (example)
    try:
        with open("data/sample_interviews.json", 'r', encoding='utf-8') as f:
            interview_data = json.load(f)
        
        # Extract questions
        questions, chunks_processed = extractor.extract_questions_from_interviews(
            interview_data, 
            chunk_size=25,
            max_chunks=None  # Process all chunks
        )
        
        # Save results
        metadata = interview_data.get('metadata', {})
        extractor.save_results(questions, metadata)
        
        # Print summary
        total_questions = sum(len(questions[cat]) for cat in questions)
        print(f"✅ Extraction complete! Found {total_questions} questions from {chunks_processed} chunks")
        
    except FileNotFoundError:
        print("❌ Sample interview data not found. Please run the scraper first.")
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")


if __name__ == "__main__":
    main()
