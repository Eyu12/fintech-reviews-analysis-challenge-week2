"""
Task 1: Data Collection - Scrape reviews from Google Play Store
Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), Dashen Bank
"""
import pandas as pd
from google_play_scraper import reviews_all, Sort
import time
import logging
from datetime import datetime
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from config import APP_IDS, SCRAPING_CONFIG, DATA_PATHS, TASK1_REQUIREMENTS
except ImportError:
    # Fallback configuration if config.py is not available
    APP_IDS = {
        'CBE': 'com.combanketh.mobilebanking',
        'BOA': 'com.boa.boaMobileBanking', 
        'DASHEN': 'com.dashen.dashensuperapp'
    }
    
    SCRAPING_CONFIG = {
        'lang': 'en',
        'country': 'us', 
        'sleep_between_requests': 2,
        'retry_delay': 5
    }
    
    DATA_PATHS = {
        'raw_reviews': '../data/raw/reviews_raw.csv'
    }
    
    TASK1_REQUIREMENTS = {
        'total_min_reviews': 1000,
        'min_reviews_per_bank': 100,
        'required_columns': ['review_id', 'review_text', 'rating', 'date', 'bank', 'source']
    }

# Set up logging with proper encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scraping.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)  # Use stdout for better encoding support
    ]
)
logger = logging.getLogger(__name__)

class BankReviewsScraper:
    def __init__(self):
        self.app_ids = APP_IDS
        self.config = SCRAPING_CONFIG
        self.all_reviews = []
        
    def scrape_bank_reviews(self, bank_name, app_id):
        """Scrape reviews for a specific bank app"""
        logger.info(f"Starting to scrape reviews for {bank_name} ({app_id})")
        
        try:
            # Scrape reviews from Google Play Store
            bank_reviews = reviews_all(
                app_id,
                lang=self.config['lang'],
                country=self.config['country'],
                sort=Sort.MOST_RELEVANT,
                sleep_milliseconds=self.config['sleep_between_requests'] * 1000,
            )
            
            # Process and format reviews
            processed_count = 0
            for review in bank_reviews:
                review_data = {
                    'review_id': review['reviewId'],
                    'review_text': review['content'],
                    'rating': review['score'],
                    'date': review['at'].strftime('%Y-%m-%d'),
                    'bank': bank_name,
                    'source': 'Google Play Store',
                    'thumbs_up': review['thumbsUpCount'],
                    'review_created_version': review.get('reviewCreatedVersion', ''),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                self.all_reviews.append(review_data)
                processed_count += 1
            
            logger.info(f"Successfully scraped {processed_count} reviews for {bank_name}")
            return processed_count
            
        except Exception as e:
            logger.error(f"Failed to scrape {bank_name}: {e}")
            return 0
    
    def scrape_all_banks(self):
        """Scrape reviews for all banks"""
        logger.info("Starting scraping process for all banks...")
        
        total_reviews = 0
        for bank_name, app_id in self.app_ids.items():
            reviews_count = self.scrape_bank_reviews(bank_name, app_id)
            total_reviews += reviews_count
            
            # Be polite to Google's servers
            if bank_name != list(self.app_ids.keys())[-1]:  # Not the last bank
                time.sleep(self.config['retry_delay'])
        
        logger.info(f"Scraping completed! Total reviews: {total_reviews}")
        return total_reviews
    
    def save_raw_data(self):
        """Save raw scraped data to CSV"""
        if not self.all_reviews:
            logger.warning("No reviews to save!")
            return None
        
        df = pd.DataFrame(self.all_reviews)
        
        # Create directories if they don't exist
        raw_dir = os.path.dirname(DATA_PATHS['raw_reviews'])
        os.makedirs(raw_dir, exist_ok=True)
        
        # Save with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/raw/reviews_raw_{timestamp}.csv"
        
        # Create directory for timestamped file too
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Save both files
        df.to_csv(filename, index=False, encoding='utf-8')
        df.to_csv(DATA_PATHS['raw_reviews'], index=False, encoding='utf-8')
        
        logger.info(f"Raw data saved to: {filename}")
        logger.info(f"Main raw file updated: {DATA_PATHS['raw_reviews']}")
        
        return df
    
    def generate_scraping_report(self):
        """Generate a scraping summary report"""
        if not self.all_reviews:
            return None
        
        df = pd.DataFrame(self.all_reviews)
        report = {
            'total_reviews': len(df),
            'reviews_per_bank': df['bank'].value_counts().to_dict(),
            'rating_distribution': df['rating'].value_counts().sort_index().to_dict(),
            'date_range': {
                'earliest': df['date'].min(),
                'latest': df['date'].max()
            },
            'scraping_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Check if requirements are met
        requirements_met = all([
            len(df) >= TASK1_REQUIREMENTS['total_min_reviews'],
            all(count >= TASK1_REQUIREMENTS['min_reviews_per_bank'] 
                for count in report['reviews_per_bank'].values())
        ])
        
        report['requirements_met'] = requirements_met
        report['missing_columns'] = [col for col in TASK1_REQUIREMENTS['required_columns'] 
                                   if col not in df.columns]
        
        return report

def main():
    """Main scraping function"""
    print("=" * 60)
    print("TASK 1: GOOGLE PLAY STORE REVIEWS SCRAPING")
    print("=" * 60)
    print("Target Banks:")
    print("  - Commercial Bank of Ethiopia (CBE)")
    print("  - Bank of Abyssinia (BOA)")
    print("  - Dashen Bank")
    print("=" * 60)
    
    # Create necessary directories
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    # Initialize scraper
    scraper = BankReviewsScraper()
    
    # Start scraping
    total_reviews = scraper.scrape_all_banks()
    
    if total_reviews > 0:
        # Save data
        df = scraper.save_raw_data()
        
        # Generate report
        report = scraper.generate_scraping_report()
        
        print("\n" + "=" * 40)
        print("SCRAPING REPORT")
        print("=" * 40)
        print(f"Total Reviews: {report['total_reviews']}")
        print(f"Reviews per Bank:")
        for bank, count in report['reviews_per_bank'].items():
            print(f"  - {bank}: {count} reviews")
        
        print(f"Rating Distribution: {report['rating_distribution']}")
        print(f"Date Range: {report['date_range']['earliest']} to {report['date_range']['latest']}")
        print(f"Requirements Met: {'YES' if report['requirements_met'] else 'NO'}")
        
        if report['missing_columns']:
            print(f"Missing Columns: {report['missing_columns']}")
        
        print(f"\nData saved to: {DATA_PATHS['raw_reviews']}")
        
    else:
        print("No reviews were scraped. Please check the logs for errors.")

if __name__ == "__main__":
    main()