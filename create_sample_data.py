import pandas as pd
import json
from datetime import datetime, timedelta

# Create sample student data with multiple grades and classes
data = {
    'student_id': [],
    'student_name': [],
    'grade': [],
    'class_section': [],
    'homework_title': [],
    'submission_status': [],
    'submission_date': [],
    'quiz_name': [],
    'quiz_score': [],
    'quiz_date': [],
    'quiz_scheduled_date': []
}

# Sample students across different grades
students = [
    # Grade 8, Section A
    ('S001', 'Aarav Kumar', 8, 'A'),
    ('S002', 'Priya Sharma', 8, 'A'),
    ('S003', 'Rohan Patel', 8, 'A'),
    ('S004', 'Ananya Singh', 8, 'A'),
    ('S005', 'Arjun Reddy', 8, 'A'),
    # Grade 8, Section B
    ('S006', 'Diya Gupta', 8, 'B'),
    ('S007', 'Kabir Mehta', 8, 'B'),
    ('S008', 'Ishaan Verma', 8, 'B'),
    # Grade 9, Section A
    ('S009', 'Sanya Joshi', 9, 'A'),
    ('S010', 'Vihaan Desai', 9, 'A'),
    ('S011', 'Aisha Khan', 9, 'A'),
    # Grade 10, Section A
    ('S012', 'Raj Malhotra', 10, 'A'),
    ('S013', 'Meera Iyer', 10, 'A'),
]

# Homework assignments
homeworks = [
    'Math Chapter 5 Exercise',
    'Science Lab Report',
    'English Essay on Climate Change',
    'History Project on Independence',
]

# Quiz information
quizzes = [
    ('Math Quiz 1', datetime.now() - timedelta(days=5)),
    ('Science Quiz 2', datetime.now() - timedelta(days=3)),
    ('English Quiz 1', datetime.now() - timedelta(days=7)),
]

# Upcoming quizzes
upcoming_quizzes = [
    ('Math Quiz 2', datetime.now() + timedelta(days=3)),
    ('Science Quiz 3', datetime.now() + timedelta(days=5)),
    ('History Quiz 1', datetime.now() + timedelta(days=8)),
]

# Generate data for each student
for student_id, name, grade, section in students:
    for hw in homeworks:
        # Randomly assign submission status
        import random
        submitted = random.choice([True, True, False])  # 66% submission rate
        
        data['student_id'].append(student_id)
        data['student_name'].append(name)
        data['grade'].append(grade)
        data['class_section'].append(section)
        data['homework_title'].append(hw)
        data['submission_status'].append('Submitted' if submitted else 'Not Submitted')
        data['submission_date'].append(
            (datetime.now() - timedelta(days=random.randint(1, 7))).strftime('%Y-%m-%d')
            if submitted else 'N/A'
        )
        
        # Quiz data for past quizzes
        quiz_name, quiz_date = random.choice(quizzes)
        data['quiz_name'].append(quiz_name)
        data['quiz_score'].append(random.randint(60, 100) if submitted else 'N/A')
        data['quiz_date'].append(quiz_date.strftime('%Y-%m-%d'))
        
        # Upcoming quiz
        upcoming_quiz, scheduled_date = random.choice(upcoming_quizzes)
        data['quiz_scheduled_date'].append(scheduled_date.strftime('%Y-%m-%d'))

# Create DataFrame
df = pd.DataFrame(data)

# Save as CSV
df.to_csv('student_data.csv', index=False)
print("✅ Created student_data.csv")

# Also save as JSON for alternative format
df.to_json('student_data.json', orient='records', indent=2)
print("✅ Created student_data.json")

# Display summary
print(f"\n📊 Dataset Summary:")
print(f"Total records: {len(df)}")
print(f"Grades: {sorted(df['grade'].unique())}")
print(f"Total students: {df['student_name'].nunique()}")
print(f"\nFirst few rows:")
print(df.head())