"""
Task 1: Data Preprocessing - Clean and prepare scraped reviews
Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), Dashen Bank
"""
import pandas as pd
import numpy as np
import re
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from config import PROCESSING_CONFIG, DATA_PATHS, TASK1_REQUIREMENTS
except ImportError:
    # Fallback configuration if config.py is not available
    PROCESSING_CONFIG = {
        'allowed_ratings': [1, 2, 3, 4, 5],
        'min_review_length': 3,
        'max_review_length': 1000,
        'text_cleaning': {
            'remove_special_chars': True,
            'remove_emojis': True
        }
    }
    
    DATA_PATHS = {
        'raw_reviews': '../data/raw/reviews_raw.csv',
        'processed_reviews': '../data/processed/reviews_processed.csv'
    }
    
    TASK1_REQUIREMENTS = {
        'total_min_reviews': 1000,
        'min_reviews_per_bank': 100,
        'max_data_errors': 0.3,
        'required_columns': ['review_id', 'review_text', 'rating', 'date', 'bank', 'source'],
        'date_format': '%Y-%m-%d'
    }

# Set up logging with proper encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/preprocessing.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)  # Use stdout for better encoding support
    ]
)
logger = logging.getLogger(__name__)

class DataPreprocessor:
    def __init__(self):
        self.config = PROCESSING_CONFIG
        self.requirements = TASK1_REQUIREMENTS
    
    def load_raw_data(self, filepath=None):
        """Load raw scraped data"""
        if filepath is None:
            filepath = DATA_PATHS['raw_reviews']
        
        try:
            df = pd.read_csv(filepath)
            logger.info(f"Loaded {len(df)} reviews from {filepath}")
            return df
        except FileNotFoundError:
            logger.error(f"Raw data file not found: {filepath}")
            return None
    
    def validate_data_structure(self, df):
        """Validate that data has required structure"""
        logger.info("Validating data structure...")
        
        # Check required columns
        missing_columns = [col for col in self.requirements['required_columns'] 
                         if col not in df.columns]
        
        if missing_columns:
            logger.error(f"Missing required columns: {missing_columns}")
            return False
        
        logger.info("All required columns present")
        return True
    
    def remove_duplicates(self, df):
        """Remove duplicate reviews"""
        initial_count = len(df)
        df_clean = df.drop_duplicates(subset=['review_text', 'bank', 'rating'])
        removed_count = initial_count - len(df_clean)
        
        logger.info(f"Removed {removed_count} duplicate reviews")
        return df_clean
    
    def handle_missing_values(self, df):
        """Handle missing values in the dataset"""
        initial_count = len(df)
        
        # Log missing values before cleaning
        missing_before = df.isnull().sum()
        if missing_before.sum() > 0:
            logger.info("Missing values before cleaning:")
            for col, count in missing_before.items():
                if count > 0:
                    logger.info(f"  - {col}: {count} missing")
        
        # Remove rows with missing critical data
        df_clean = df.dropna(subset=['review_text', 'rating', 'bank'])
        
        # Fill other missing values if appropriate
        df_clean = df_clean.copy()  # Avoid SettingWithCopyWarning
        df_clean.loc[:, 'review_created_version'] = df_clean['review_created_version'].fillna('Unknown')
        df_clean.loc[:, 'thumbs_up'] = df_clean['thumbs_up'].fillna(0)
        
        removed_count = initial_count - len(df_clean)
        logger.info(f"Removed {removed_count} rows with missing critical data")
        
        return df_clean
    
    def clean_text(self, text):
        """Clean and normalize review text"""
        if pd.isna(text):
            return ""
        
        text = str(text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        if self.config['text_cleaning']['remove_special_chars']:
            text = re.sub(r'[^\w\s.,!?]', '', text)
        
        # Remove emojis
        if self.config['text_cleaning']['remove_emojis']:
            emoji_pattern = re.compile(
                "["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                "]+", flags=re.UNICODE
            )
            text = emoji_pattern.sub(r'', text)
        
        return text.strip()
    
    def validate_ratings(self, df):
        """Validate and clean rating values"""
        initial_count = len(df)
        
        # Convert to numeric and remove invalid ratings
        df_clean = df.copy()
        df_clean['rating'] = pd.to_numeric(df_clean['rating'], errors='coerce')
        df_clean = df_clean[df_clean['rating'].isin(self.config['allowed_ratings'])]
        
        removed_count = initial_count - len(df_clean)
        logger.info(f"Removed {removed_count} rows with invalid ratings")
        
        return df_clean
    
    def validate_dates(self, df):
        """Validate and standardize date format"""
        df_clean = df.copy()
        
        # Convert to datetime
        df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        
        # Remove invalid dates
        invalid_dates = df_clean['date'].isna().sum()
        if invalid_dates > 0:
            logger.warning(f"Found {invalid_dates} reviews with invalid dates")
            df_clean = df_clean.dropna(subset=['date'])
        
        # Standardize date format
        df_clean['date'] = df_clean['date'].dt.strftime(self.requirements['date_format'])
        
        logger.info("Dates validated and standardized")
        return df_clean
    
    def filter_by_length(self, df):
        """Filter reviews by length requirements"""
        initial_count = len(df)
        
        df_clean = df.copy()
        df_clean['review_length'] = df_clean['review_text'].str.len()
        
        # Filter by length
        mask = (df_clean['review_length'] >= self.config['min_review_length']) & \
               (df_clean['review_length'] <= self.config['max_review_length'])
        
        df_clean = df_clean[mask]
        
        removed_count = initial_count - len(df_clean)
        logger.info(f"Removed {removed_count} reviews outside length limits")
        
        return df_clean
    
    def preprocess_data(self, df):
        """Main preprocessing pipeline"""
        logger.info("Starting data preprocessing pipeline...")
        
        # Step 1: Remove duplicates
        df_clean = self.remove_duplicates(df)
        
        # Step 2: Handle missing values
        df_clean = self.handle_missing_values(df_clean)
        
        # Step 3: Clean text
        df_clean['cleaned_review'] = df_clean['review_text'].apply(self.clean_text)
        
        # Step 4: Validate ratings
        df_clean = self.validate_ratings(df_clean)
        
        # Step 5: Validate dates
        df_clean = self.validate_dates(df_clean)
        
        # Step 6: Filter by length
        df_clean = self.filter_by_length(df_clean)
        
        # Add derived columns
        df_clean['word_count'] = df_clean['cleaned_review'].str.split().str.len()
        df_clean['processing_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info("Preprocessing pipeline completed")
        return df_clean
    
    def save_processed_data(self, df):
        """Save processed data to CSV"""
        # Create directories if they don't exist
        processed_dir = os.path.dirname(DATA_PATHS['processed_reviews'])
        os.makedirs(processed_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save with timestamp
        filename = f"data/processed/reviews_processed_{timestamp}.csv"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save both files
        df.to_csv(filename, index=False, encoding='utf-8')
        df.to_csv(DATA_PATHS['processed_reviews'], index=False, encoding='utf-8')
        
        logger.info(f"Processed data saved to: {filename}")
        logger.info(f"Main processed file updated: {DATA_PATHS['processed_reviews']}")
        
        return filename
    
    def generate_quality_report(self, df_raw, df_processed):
        """Generate data quality report"""
        report = {
            'initial_reviews': len(df_raw),
            'final_reviews': len(df_processed),
            'reviews_removed': len(df_raw) - len(df_processed),
            'removal_rate': (len(df_raw) - len(df_processed)) / len(df_raw) * 100,
            'reviews_per_bank': df_processed['bank'].value_counts().to_dict(),
            'rating_distribution': df_processed['rating'].value_counts().sort_index().to_dict(),
            'data_quality_metrics': {
                'duplicates_removed': len(df_raw) - len(self.remove_duplicates(df_raw)),
                'missing_values_removed': df_raw.isnull().sum().sum() - df_processed.isnull().sum().sum(),
                'invalid_ratings_removed': len(df_raw) - len(self.validate_ratings(df_raw)),
                'date_issues_fixed': df_raw['date'].isna().sum() - df_processed['date'].isna().sum()
            },
            'text_statistics': {
                'avg_review_length': df_processed['cleaned_review'].str.len().mean(),
                'avg_word_count': df_processed['word_count'].mean(),
                'total_words': df_processed['word_count'].sum()
            }
        }
        
        # Check if requirements are met
        report['requirements_met'] = all([
            report['final_reviews'] >= self.requirements['total_min_reviews'],
            all(count >= self.requirements['min_reviews_per_bank'] 
                for count in report['reviews_per_bank'].values()),
            report['removal_rate'] <= self.requirements['max_data_errors'] * 100
        ])
        
        return report

def main():
    """Main preprocessing function"""
    print("=" * 60)
    print("TASK 1: DATA PREPROCESSING & CLEANING")
    print("=" * 60)
    print("Processing Banks:")
    print("  - Commercial Bank of Ethiopia (CBE)")
    print("  - Bank of Abyssinia (BOA)")
    print("  - Dashen Bank")
    print("=" * 60)
    
    # Create necessary directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Load raw data
    df_raw = preprocessor.load_raw_data()
    if df_raw is None:
        print("Cannot proceed without raw data. Please run scraper first.")
        return
    
    # Validate data structure
    if not preprocessor.validate_data_structure(df_raw):
        print("Data structure validation failed.")
        return
    
    # Preprocess data
    df_processed = preprocessor.preprocess_data(df_raw)
    
    if len(df_processed) > 0:
        # Save processed data
        filename = preprocessor.save_processed_data(df_processed)
        
        # Generate quality report
        report = preprocessor.generate_quality_report(df_raw, df_processed)
        
        print("\n" + "=" * 40)
        print("DATA QUALITY REPORT")
        print("=" * 40)
        print(f"Initial Reviews: {report['initial_reviews']}")
        print(f"Final Reviews: {report['final_reviews']}")
        print(f"Reviews Removed: {report['reviews_removed']} ({report['removal_rate']:.2f}%)")
        
        print(f"\nReviews per Bank:")
        for bank, count in report['reviews_per_bank'].items():
            status = "✓" if count >= TASK1_REQUIREMENTS['min_reviews_per_bank'] else "✗"
            print(f"  {status} {bank}: {count} reviews")
        
        print(f"\nRating Distribution:")
        for rating, count in report['rating_distribution'].items():
            print(f"  {rating} stars: {count} reviews")
        
        print(f"\nText Statistics:")
        print(f"  Average Review Length: {report['text_statistics']['avg_review_length']:.1f} chars")
        print(f"  Average Word Count: {report['text_statistics']['avg_word_count']:.1f} words")
        
        print(f"\nRequirements Met: {'YES' if report['requirements_met'] else 'NO'}")
        print(f"Processed data saved to: {filename}")
        
    else:
        print("No data remaining after preprocessing.")

if __name__ == "__main__":
    main()