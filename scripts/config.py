"""
Configuration for Bank Reviews Analysis - Task 1: Data Collection & Preprocessing
Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), Dashen Bank
"""
import os
from datetime import datetime

# =============================================================================
# GOOGLE PLAY STORE APP IDs - ETHIOPIAN BANKS
# =============================================================================
APP_IDS = {
    'CBE': 'com.combanketh.mobilebanking',  # Commercial Bank of Ethiopia
    'BOA': 'com.boa.boaMobileBanking',  # Bank of Abyssinia
    'DASHEN': 'com.dashen.dashensuperapp'  # Dashen Bank
}

BANK_NAMES = {
    'CBE': 'Commercial Bank of Ethiopia',
    'BOA': 'Bank of Abyssinia',
    'DASHEN': 'Dashen Bank'
}

# =============================================================================
# TASK 1 REQUIREMENTS
# =============================================================================
TASK1_REQUIREMENTS = {
    'min_reviews_per_bank': 400,
    'total_min_reviews': 1200,
    'max_data_errors': 0.05,  # <5% errors
    'required_columns': ['review_text', 'rating', 'date', 'bank', 'source'],
    'date_format': '%Y-%m-%d'
}

# =============================================================================
# SCRAPING CONFIGURATION
# =============================================================================
SCRAPING_CONFIG = {
    'reviews_per_bank': 500,  # Buffer for 400 minimum
    'max_retries': 3,
    'retry_delay': 10,
    'sleep_between_requests': 2,
    'lang': 'en',
    'country': 'et',
    'sort_by': 'MOST_RELEVANT'
}

# =============================================================================
# DATA PROCESSING CONFIGURATION
# =============================================================================
PROCESSING_CONFIG = {
    'min_review_length': 3,
    'max_review_length': 1000,
    'allowed_ratings': [1, 2, 3, 4, 5],
    'text_cleaning': {
        'remove_special_chars': True,
        'remove_extra_spaces': True,
        'convert_to_lowercase': False,  # Keep original case for analysis
        'remove_emojis': True
    }
}

# =============================================================================
# FILE PATHS
# =============================================================================
DATA_PATHS = {
    'raw': '../data/raw',
    'processed': '../data/processed',
    'raw_reviews': '../data/raw/reviews_raw.csv',
    'processed_reviews': '../data/processed/reviews_processed.csv',
    'cleaned_reviews': '../data/processed/reviews_cleaned.csv'
}


def create_directories():
    """Create necessary directories for Task 1"""
    directories = ['data/raw', 'data/processed', 'logs']
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created: {dir_path}")

# Initialize directories when config is imported
if __name__ != "__main__":
    create_directories()

if __name__ == "__main__":
    print(" Task 1 Configuration Loaded Successfully!")
    print(f" Banks configured: {list(BANK_NAMES.values())}")
    print(f" Target reviews per bank: {SCRAPING_CONFIG['reviews_per_bank']}")
    print(f" Total target reviews: {SCRAPING_CONFIG['reviews_per_bank'] * len(APP_IDS)}")