"""
Configuration for Task 2: Sentiment & Thematic Analysis
"""
import os


# SENTIMENT ANALYSIS CONFIGURATION

SENTIMENT_CONFIG = {
    'model_name': 'distilbert-base-uncased-finetuned-sst-2-english',
    'batch_size': 100,
    'sentiment_thresholds': {
        'positive': 0.6,
        'negative': 0.4,
        'neutral_lower': 0.4,
        'neutral_upper': 0.6
    }
}


# THEMATIC ANALYSIS CONFIGURATION  

THEMATIC_CONFIG = {
    'tfidf_max_features': 100,
    'min_keyword_frequency': 5,
    'theme_keywords': {
        'Account Access Issues': ['login', 'password', 'access', 'account', 'verify', 'authentication'],
        'Transaction Performance': ['slow', 'transfer', 'transaction', 'loading', 'speed', 'wait', 'time'],
        'UI/UX Experience': ['interface', 'design', 'easy', 'navigation', 'layout', 'user friendly'],
        'Customer Support': ['support', 'help', 'service', 'response', 'contact', 'assistance'],
        'App Reliability': ['crash', 'bug', 'error', 'freeze', 'update', 'not working'],
        'Security Concerns': ['security', 'safe', 'hack', 'privacy', 'protection'],
        'Feature Requests': ['feature', 'add', 'should have', 'missing', 'want', 'need']
    },
    'min_theme_reviews': 10
}

# FILE PATHS FOR TASK 2

TASK2_PATHS = {
    'input_data': 'data/processed/reviews_processed_20251127_172029.csv',
    'sentiment_results': 'data/results/reviews_with_sentiment.csv',
    'thematic_results': 'data/results/reviews_with_themes.csv',
    'final_results': 'data/results/reviews_final.csv',
    'analysis_summary': 'data/results/analysis_summary.csv'
}


# CREATE DIRECTORIES

def create_task2_directories():
    """Create directories for Task 2 results"""
    directories = ['data/results']
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Created: {dir_path}")

# Initialize directories
create_task2_directories()

print("✅ Task 2 Configuration Loaded Successfully!")