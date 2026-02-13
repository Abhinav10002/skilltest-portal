import os
import django

# 1. Setup Django Environment
# Make sure 'application.settings' matches the name of your main project folder
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

# 2. Import your models
from staff_portal.models import Assessment, Question, Option

def seed_database():
    print("🌱 Starting database seeding process...")

    # 3. Define the Tests and Questions
    test_data = [
        {
            "title": "Python Programming",
            "description": "Test your fundamental knowledge of Python data structures and syntax.",
            "questions": [
                {
                    "text": "Which of the following data types is immutable in Python?",
                    "options": [("List", False), ("Dictionary", False), ("Tuple", True), ("Set", False)]
                },
                {
                    "text": "What is the correct file extension for Python files?",
                    "options": [(".pt", False), (".pyt", False), (".py", True), (".txt", False)]
                },
                {
                    "text": "How do you insert a comment in Python code?",
                    "options": [("// This is a comment", False), ("# This is a comment", True), ("/* This is a comment */", False), ("", False)]
                }
            ]
        },
        {
            "title": "Machine Learning Basics",
            "description": "An introductory assessment covering core ML concepts and terminology.",
            "questions": [
                {
                    "text": "Which of the following is an example of Unsupervised Learning?",
                    "options": [("Predicting house prices", False), ("Image classification", False), ("Customer clustering", True), ("Spam detection", False)]
                },
                {
                    "text": "What does 'Overfitting' mean in Machine Learning?",
                    "options": [("Model performs well on training data but poorly on unseen data", True), ("Model performs poorly on all data", False), ("Model is too simple to capture patterns", False), ("Model needs more data to train", False)]
                },
                {
                    "text": "Which evaluation metric is typically used for classification tasks?",
                    "options": [("Mean Squared Error", False), ("Accuracy", True), ("R-squared", False), ("Root Mean Squared Error", False)]
                }
            ]
        },
        {
            "title": "General Aptitude Test",
            "description": "Evaluate logical reasoning and quantitative problem-solving skills.",
            "questions": [
                {
                    "text": "If a train travels 60 km/h, how far will it travel in 45 minutes?",
                    "options": [("40 km", False), ("45 km", True), ("50 km", False), ("60 km", False)]
                },
                {
                    "text": "What is the next number in the series: 2, 6, 12, 20, 30, ...?",
                    "options": [("36", False), ("40", False), ("42", True), ("48", False)]
                },
                {
                    "text": "A shirt originally priced at $40 is on sale for 20% off. What is the sale price?",
                    "options": [("32", True), ("30", False), ("34", False), ("38", False)]
                }
            ]
        }
    ]

    # 4. Loop through the data and create database entries
    for data in test_data:
        # Create Assessment (get_or_create prevents duplicates if you run it twice)
        assessment, created = Assessment.objects.get_or_create(
            title=data["title"],
            defaults={"description": data["description"]}
        )
        
        if created:
            print(f"✅ Created Assessment: {assessment.title}")
            
            for q_data in data["questions"]:
                # Create Question
                question = Question.objects.create(
                    assessment=assessment,
                    text=q_data["text"],
                    marks=1
                )
                
                # Create Options
                for opt_text, is_correct in q_data["options"]:
                    Option.objects.create(
                        question=question,
                        text=opt_text,
                        is_correct=is_correct
                    )
        else:
            print(f"⚠️ Skipped Assessment: {assessment.title} (Already exists)")

    print("🎉 Seeding complete! You can now view these tests on your dashboard.")

if __name__ == "__main__":
    seed_database()