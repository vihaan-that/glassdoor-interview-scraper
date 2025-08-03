"""
Basic Interview Analyzer
========================

Regex-based question extraction and analysis for interview data.
Provides a fallback option when AI extraction is not available.

Author: Interview Preparation Assistant
License: MIT
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Set
from collections import Counter
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasicInterviewAnalyzer:
    """
    Basic analyzer using regex patterns and keyword matching
    """
    
    def __init__(self, config: Dict = None):
        """
        Initialize the analyzer with configuration
        
        Args:
            config: Dictionary containing analyzer configuration
        """
        self.config = config or self._default_config()
        self.question_patterns = self._compile_question_patterns()
        self.keyword_categories = self._setup_keyword_categories()
    
    def _default_config(self) -> Dict:
        """Default configuration"""
        return {
            'min_question_length': 15,
            'max_question_length': 300,
            'remove_duplicates': True,
            'case_sensitive': False
        }
    
    def _compile_question_patterns(self) -> List[re.Pattern]:
        """Compile regex patterns for question extraction"""
        patterns = [
            r'asked\s+(?:me\s+)?(?:about\s+)?([^.!?]+[?.])',
            r'question\s+(?:was\s+)?(?:about\s+)?([^.!?]+[?.])',
            r'they\s+asked\s+([^.!?]+[?.])',
            r'interviewer\s+asked\s+([^.!?]+[?.])',
            r'was\s+asked\s+([^.!?]+[?.])',
            r'questions?\s*:\s*([^.!?]+)',
            r'problem\s*:\s*([^.!?]+)',
            r'(?:coding|technical|behavioral)\s+question[s]?\s*:\s*([^.!?]+)',
        ]
        
        flags = re.IGNORECASE if not self.config['case_sensitive'] else 0
        return [re.compile(pattern, flags) for pattern in patterns]
    
    def _setup_keyword_categories(self) -> Dict[str, List[str]]:
        """Setup keyword categories for question classification"""
        return {
            'coding_questions': [
                'algorithm', 'data structure', 'array', 'string', 'linked list', 'tree', 'graph',
                'dp', 'dynamic programming', 'recursion', 'sorting', 'searching', 'leetcode',
                'coding problem', 'programming', 'implement', 'write code', 'solve', 'hanoi',
                'scramble', 'combination', 'walls and gates', 'corona virus', 'prime numbers',
                'dfs', 'bfs', 'misplaced employees', 'password', 'interleaved', 'binary search',
                'two sum', 'palindrome', 'subset', 'backtracking', 'coin change', 'josephus'
            ],
            'technical_questions': [
                'javascript', 'python', 'java', 'sql', 'database', 'mysql', 'mongodb',
                'react', 'node', 'express', 'aws', 's3', 'linux', 'security', 'json',
                'oops', 'oop', 'dbms', 'operating system', 'design pattern', 'architecture',
                'tech stack', 'framework', 'api', 'rest', 'microservices', 'scalability',
                'mvc', 'dependency injection', 'caching', 'load balancing'
            ],
            'sql_questions': [
                'sql query', 'database query', 'join', 'inner join', 'outer join',
                'select statement', 'where clause', 'group by', 'order by', 'having',
                'subquery', 'stored procedure', 'trigger', 'index', 'normalization',
                'second highest salary', 'nth highest', 'duplicate records'
            ],
            'behavioral_questions': [
                'tell me about yourself', 'why', 'experience', 'project', 'challenge',
                'team', 'conflict', 'leadership', 'strength', 'weakness', 'goal',
                'motivation', 'difficult situation', 'achievement', 'failure',
                'time management', 'problem solving', 'communication'
            ],
            'hr_questions': [
                'salary', 'notice period', 'why company', 'why leaving', 'career',
                'company', 'role', 'expectations', 'growth', 'future', 'relocate',
                'benefits', 'work life balance', 'long term goals'
            ],
            'system_design_questions': [
                'design', 'architecture', 'system', 'scale', 'scalability',
                'high availability', 'load balancer', 'database design',
                'microservices', 'distributed system', 'chat application',
                'notification system', 'url shortener'
            ],
            'project_questions': [
                'previous project', 'last project', 'current project', 'project experience',
                'project architecture', 'project challenges', 'technologies used',
                'project timeline', 'project team', 'project outcome'
            ]
        }
    
    def analyze_interviews(self, interview_data: Dict) -> Dict:
        """
        Analyze interview data and extract categorized questions
        
        Args:
            interview_data: Dictionary containing interview reviews
            
        Returns:
            Dictionary containing analyzed results
        """
        interviews = interview_data.get('interviews', [])
        if not interviews:
            raise ValueError("No interviews found in data")
        
        logger.info(f"📊 Analyzing {len(interviews)} interviews...")
        
        # Extract questions from all interviews
        all_questions = self._extract_all_questions(interviews)
        
        # Categorize questions
        categorized_questions = self._categorize_questions(all_questions)
        
        # Generate statistics
        stats = self._generate_statistics(interviews, categorized_questions)
        
        # Generate study plan
        study_plan = self._generate_study_plan(categorized_questions, stats)
        
        return {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'total_interviews': len(interviews),
                'total_questions_extracted': sum(len(cat) for cat in categorized_questions.values()),
                'analyzer_type': 'basic_regex'
            },
            'questions': categorized_questions,
            'statistics': stats,
            'study_plan': study_plan
        }
    
    def _extract_all_questions(self, interviews: List[Dict]) -> Set[str]:
        """Extract questions from all interviews using regex patterns"""
        all_questions = set()
        
        for interview in interviews:
            text = interview.get('raw_text', '').lower()
            
            # Apply all question patterns
            for pattern in self.question_patterns:
                matches = pattern.findall(text)
                for match in matches:
                    question = self._clean_question(match)
                    if self._is_valid_question(question):
                        all_questions.add(question)
        
        logger.info(f"📋 Extracted {len(all_questions)} unique questions")
        return all_questions
    
    def _clean_question(self, question: str) -> str:
        """Clean and normalize a question"""
        # Remove extra whitespace and punctuation
        question = re.sub(r'\s+', ' ', question.strip())
        question = question.strip('.,!?').strip()
        
        # Capitalize first letter
        if question:
            question = question[0].upper() + question[1:]
        
        return question
    
    def _is_valid_question(self, question: str) -> bool:
        """Check if a question meets quality criteria"""
        if not question:
            return False
        
        length = len(question)
        if length < self.config['min_question_length'] or length > self.config['max_question_length']:
            return False
        
        # Skip questions with too many special characters
        special_char_ratio = sum(1 for c in question if not c.isalnum() and c != ' ') / length
        if special_char_ratio > 0.3:
            return False
        
        return True
    
    def _categorize_questions(self, questions: Set[str]) -> Dict[str, List[str]]:
        """Categorize questions based on keywords"""
        categorized = {category: [] for category in self.keyword_categories}
        uncategorized = []
        
        for question in questions:
            question_lower = question.lower()
            categorized_flag = False
            
            # Check each category
            for category, keywords in self.keyword_categories.items():
                if any(keyword in question_lower for keyword in keywords):
                    categorized[category].append(question)
                    categorized_flag = True
                    break
            
            if not categorized_flag:
                uncategorized.append(question)
        
        # Add uncategorized to technical by default
        categorized['technical_questions'].extend(uncategorized)
        
        # Sort questions in each category
        for category in categorized:
            categorized[category].sort()
        
        return categorized
    
    def _generate_statistics(self, interviews: List[Dict], questions: Dict) -> Dict:
        """Generate analysis statistics"""
        # Count technical topics mentioned
        technical_topics = Counter()
        difficulty_distribution = Counter()
        outcome_distribution = Counter()
        
        for interview in interviews:
            text = interview.get('raw_text', '').lower()
            
            # Count technical keywords
            for keyword in self.keyword_categories['technical_questions']:
                if keyword in text:
                    technical_topics[keyword] += 1
            
            # Count difficulty levels
            difficulty = interview.get('difficulty', 'Not specified')
            difficulty_distribution[difficulty] += 1
            
            # Count outcomes
            outcome = interview.get('outcome', 'Not specified')
            outcome_distribution[outcome] += 1
        
        return {
            'top_technical_topics': dict(technical_topics.most_common(10)),
            'difficulty_distribution': dict(difficulty_distribution),
            'outcome_distribution': dict(outcome_distribution),
            'questions_per_category': {cat: len(qs) for cat, qs in questions.items()},
            'total_unique_questions': sum(len(qs) for qs in questions.values())
        }
    
    def _generate_study_plan(self, questions: Dict, stats: Dict) -> Dict:
        """Generate a study plan based on analysis"""
        return {
            'high_priority': [
                'Data Structures & Algorithms',
                'JavaScript fundamentals',
                'SQL queries and database concepts',
                'Previous project discussions'
            ],
            'medium_priority': [
                'System design basics',
                'Behavioral question frameworks',
                'Company research'
            ],
            'low_priority': [
                'Advanced system design',
                'Niche technologies',
                'Complex algorithms'
            ],
            'recommended_practice': {
                'coding_questions': min(len(questions['coding_questions']), 20),
                'technical_questions': min(len(questions['technical_questions']), 15),
                'behavioral_questions': min(len(questions['behavioral_questions']), 10)
            }
        }
    
    def save_results(self, results: Dict, output_dir: str = "output"):
        """Save analysis results to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save as JSON
        json_filename = f"{output_dir}/basic_analysis_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save as readable text
        txt_filename = f"{output_dir}/basic_analysis_{timestamp}.txt"
        self._save_readable_format(results, txt_filename)
        
        logger.info(f"💾 Results saved to:")
        logger.info(f"   • {json_filename}")
        logger.info(f"   • {txt_filename}")
        
        return json_filename, txt_filename
    
    def _save_readable_format(self, results: Dict, filename: str):
        """Save results in human-readable format"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("📊 BASIC INTERVIEW ANALYSIS RESULTS\n")
            f.write("=" * 45 + "\n")
            f.write(f"📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"📊 Total interviews: {results['metadata']['total_interviews']}\n")
            f.write(f"🎯 Total questions: {results['metadata']['total_questions_extracted']}\n\n")
            
            # Questions by category
            questions = results['questions']
            categories = [
                ("💻 CODING QUESTIONS", "coding_questions"),
                ("🛠️ TECHNICAL QUESTIONS", "technical_questions"),
                ("🗄️ SQL QUESTIONS", "sql_questions"),
                ("🗣️ BEHAVIORAL QUESTIONS", "behavioral_questions"),
                ("👔 HR QUESTIONS", "hr_questions"),
                ("🏗️ SYSTEM DESIGN QUESTIONS", "system_design_questions"),
                ("📋 PROJECT QUESTIONS", "project_questions")
            ]
            
            for title, key in categories:
                question_list = questions.get(key, [])
                if not question_list:
                    continue
                    
                f.write(f"{title}\n")
                f.write("=" * len(title) + "\n")
                
                for i, q in enumerate(question_list, 1):
                    f.write(f"{i:2d}. {q}\n")
                f.write(f"\nTotal: {len(question_list)} questions\n\n")
            
            # Statistics
            stats = results['statistics']
            f.write("📊 ANALYSIS STATISTICS\n")
            f.write("=" * 25 + "\n")
            f.write("🔥 Top Technical Topics:\n")
            for topic, count in list(stats['top_technical_topics'].items())[:5]:
                f.write(f"   • {topic}: {count} mentions\n")
            
            f.write(f"\n📈 Difficulty Distribution:\n")
            for difficulty, count in stats['difficulty_distribution'].items():
                f.write(f"   • {difficulty}: {count} interviews\n")
            
            # Study plan
            study_plan = results['study_plan']
            f.write(f"\n🎯 RECOMMENDED STUDY PLAN\n")
            f.write("=" * 30 + "\n")
            f.write("🔥 High Priority:\n")
            for item in study_plan['high_priority']:
                f.write(f"   • {item}\n")
            
            f.write(f"\n📊 Medium Priority:\n")
            for item in study_plan['medium_priority']:
                f.write(f"   • {item}\n")


def main():
    """Example usage of the basic analyzer"""
    try:
        # Load interview data
        with open("data/sample_interviews.json", 'r', encoding='utf-8') as f:
            interview_data = json.load(f)
        
        # Initialize analyzer
        analyzer = BasicInterviewAnalyzer()
        
        # Analyze interviews
        results = analyzer.analyze_interviews(interview_data)
        
        # Save results
        analyzer.save_results(results)
        
        # Print summary
        total_questions = results['metadata']['total_questions_extracted']
        print(f"✅ Analysis complete! Extracted {total_questions} questions")
        
    except FileNotFoundError:
        print("❌ Sample interview data not found. Please run the scraper first.")
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")


if __name__ == "__main__":
    main()
