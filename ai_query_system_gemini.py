import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class AdminQuerySystem:
    """
    AI-powered query system with role-based access control.
    Uses Google Gemini API - AUTOMATICALLY FINDS BEST MODEL
    """
    
    def __init__(self, api_key=None, admin_grade=None, admin_class=None):
        """
        Initialize the query system with admin permissions.
        
        Args:
            api_key: Gemini API key
            admin_grade: Grade the admin has access to (e.g., 8, 9, 10)
            admin_class: Class section the admin has access to (e.g., 'A', 'B')
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.admin_grade = admin_grade
        self.admin_class = admin_class
        
        if not self.api_key:
            raise ValueError("Gemini API key is required!")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Automatically find and use the best available model
        self.model = self._get_best_model()
        
        # Load the full dataset
        self.full_data = pd.read_csv('student_data.csv')
        
        # Filter data based on admin's access rights
        self.filtered_data = self._apply_role_filters()
    
    def _get_best_model(self):
        """Automatically find the best available model"""
        print("🔍 Finding best available Gemini model...")
        
        # Try models in order of preference
        preferred_models = [
            'gemini-1.5-pro-latest',
            'gemini-1.5-pro',
            'gemini-1.5-flash-latest', 
            'gemini-1.5-flash',
            'gemini-pro',
            'models/gemini-pro',
            'models/gemini-1.5-flash',
            'models/gemini-1.5-pro'
        ]
        
        # Get list of available models
        try:
            available_models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
            
            print(f"📋 Found {len(available_models)} available models")
            
            # Try to use preferred models
            for preferred in preferred_models:
                for available in available_models:
                    if preferred in available:
                        print(f"✅ Using model: {available}")
                        return genai.GenerativeModel(available)
            
            # If no preferred model found, use the first available
            if available_models:
                model_name = available_models[0]
                print(f"✅ Using model: {model_name}")
                return genai.GenerativeModel(model_name)
            
        except Exception as e:
            print(f"⚠️ Error listing models: {e}")
        
        # Fallback to gemini-pro (most common)
        print("⚠️ Using fallback model: gemini-pro")
        return genai.GenerativeModel('gemini-pro')
    
    def _apply_role_filters(self):
        """Filter the dataset based on admin's access rights."""
        df = self.full_data.copy()
        
        if self.admin_grade is not None:
            df = df[df['grade'] == self.admin_grade]
        
        if self.admin_class is not None:
            df = df[df['class_section'] == self.admin_class]
        
        return df
    
    def get_access_info(self):
        """Return information about admin's access rights."""
        info = {
            'grade': self.admin_grade or 'All grades',
            'class': self.admin_class or 'All classes',
            'total_records': len(self.filtered_data),
            'total_students': self.filtered_data['student_name'].nunique()
        }
        return info
    
    def _create_data_summary(self):
        """Create a summary of the data for the AI."""
        df = self.filtered_data
        
        # Get unique students
        students = df[['student_name', 'grade', 'class_section']].drop_duplicates()
        
        # Homework summary
        hw_summary = df.groupby(['student_name', 'homework_title', 'submission_status']).size().reset_index(name='count')
        
        # Quiz summary - handle N/A values
        quiz_data = df[['student_name', 'quiz_name', 'quiz_score']].copy()
        quiz_data = quiz_data[quiz_data['quiz_score'] != 'N/A']
        
        return {
            'total_students': len(students),
            'students_list': students['student_name'].tolist(),
            'homework_data': hw_summary.to_dict('records')[:50],
            'quiz_data': quiz_data.to_dict('records')[:50],
            'columns': list(df.columns),
            'sample_data': df.head(20).to_dict('records')
        }
    
    def query(self, question):
        """
        Process a natural language query and return results.
        
        Args:
            question: Natural language question from the admin
            
        Returns:
            Answer to the query based on filtered data
        """
        try:
            # Get data summary
            data_summary = self._create_data_summary()
            
            # Create the prompt
            prompt = f"""You are a helpful AI assistant analyzing student data for a school administrator.

Your task: Answer the following question based on the provided student data.

QUESTION: {question}

DATA AVAILABLE:
- Total Students: {data_summary['total_students']}
- Students: {', '.join(data_summary['students_list'])}

COLUMNS IN DATASET:
- student_id, student_name, grade, class_section
- homework_title, submission_status, submission_date
- quiz_name, quiz_score, quiz_date, quiz_scheduled_date

HOMEWORK SUBMISSION DATA (sample):
{json.dumps(data_summary['homework_data'][:30], indent=2)}

QUIZ SCORE DATA (sample):
{json.dumps(data_summary['quiz_data'][:30], indent=2)}

FULL SAMPLE DATA:
{json.dumps(data_summary['sample_data'], indent=2)}

INSTRUCTIONS:
1. Answer the question clearly and concisely
2. List specific student names when relevant
3. For "not submitted" queries, look for submission_status = 'Not Submitted'
4. For quiz scores, ignore entries with 'N/A' values
5. Calculate averages only from numeric quiz scores
6. Use bullet points or numbered lists for clarity when listing multiple items
7. Be specific with numbers and percentages

Provide a clear, helpful answer now:"""

            # Generate response using Gemini
            response = self.model.generate_content(prompt)
            
            return response.text
        
        except Exception as e:
            return f"❌ Error processing query: {str(e)}\n\nPlease try rephrasing your question."
    
    def get_data_summary(self):
        """Get a summary of accessible data."""
        df = self.filtered_data
        
        # Calculate submission rate
        submitted_count = (df['submission_status'] == 'Submitted').sum()
        total_count = len(df)
        submission_rate = (submitted_count / total_count * 100) if total_count > 0 else 0
        
        summary = f"""
📊 Data Access Summary:
- Grade: {self.admin_grade or 'All'}
- Class: {self.admin_class or 'All'}
- Total Students: {df['student_name'].nunique()}
- Total Records: {len(df)}
- Submission Rate: {submission_rate:.1f}%
        """
        return summary


def main():
    """Example usage with automatic model selection"""
    print("🎓 Dumroo AI Query System - Gemini (Auto Model)\n")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Please set GEMINI_API_KEY in your .env file")
        print("\nTo get a free Gemini API key:")
        print("1. Visit: https://aistudio.google.com/app/apikey")
        print("2. Sign in with your Google account")
        print("3. Click 'Get API Key' or 'Create API Key'")
        print("4. Copy the key and add it to your .env file")
        return
    
    print("Creating admin with access to Grade 8, Class A...")
    try:
        admin_system = AdminQuerySystem(
            api_key=api_key,
            admin_grade=8,
            admin_class='A'
        )
        
        access_info = admin_system.get_access_info()
        print(f"\n✅ Admin Access:")
        print(f"   Grade: {access_info['grade']}")
        print(f"   Class: {access_info['class']}")
        print(f"   Students: {access_info['total_students']}")
        print(f"   Records: {access_info['total_records']}")
        
        example_queries = [
            "Which students haven't submitted their homework yet?",
            "Show me the average quiz scores for my students",
            "List all students who scored below 70 in quizzes"
        ]
        
        print("\n" + "="*60)
        print("Running Example Queries:")
        print("="*60)
        
        for i, query in enumerate(example_queries, 1):
            print(f"\n🔍 Query {i}: {query}")
            print("-" * 60)
            result = admin_system.query(query)
            print(f"💬 Answer:\n{result}")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Check if your API key is correct")
        print("  2. Make sure you have internet connection")
        print("  3. Try running: python list_available_models.py")

if __name__ == "__main__":
    main()