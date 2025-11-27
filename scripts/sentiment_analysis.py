"""
Task 2: Sentiment Analysis using DistilBERT - FIXED VERSION
"""
import pandas as pd
import logging
from transformers import pipeline
from task2_config import SENTIMENT_CONFIG, TASK2_PATHS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.config = SENTIMENT_CONFIG
        self.sentiment_pipeline = None
        
    def load_model(self):
        """Load the DistilBERT sentiment analysis model"""
        try:
            logger.info("🔄 Loading DistilBERT sentiment model...")
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model=self.config['model_name'],
                truncation=True
            )
            logger.info("✅ Sentiment model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            return False
    
    def analyze_sentiment_safe(self, text):
        """Analyze sentiment for a single text safely"""
        if not text or pd.isna(text) or str(text).strip() == '':
            return {'label': 'NEUTRAL', 'score': 0.5}
        
        try:
            result = self.sentiment_pipeline(str(text))[0]
            return result
        except:
            return {'label': 'NEUTRAL', 'score': 0.5}
    
    def classify_sentiment(self, label, score):
        """Classify sentiment based on thresholds"""
        if label == 'POSITIVE' and score >= self.config['sentiment_thresholds']['positive']:
            return 'positive'
        elif label == 'NEGATIVE' and score <= self.config['sentiment_thresholds']['negative']:
            return 'negative'
        else:
            return 'neutral'
    
    def analyze_reviews_simple(self, df):
        """Simple and safe sentiment analysis"""
        if not self.sentiment_pipeline:
            logger.error("Model not loaded")
            return df
        
        logger.info("🎯 Starting sentiment analysis...")
        
        sentiment_labels = []
        sentiment_scores = []
        sentiment_categories = []
        
        total = len(df)
        for i, review in enumerate(df['cleaned_review']):
            result = self.analyze_sentiment_safe(review)
            
            sentiment_labels.append(result['label'])
            sentiment_scores.append(result['score'])
            sentiment_categories.append(self.classify_sentiment(result['label'], result['score']))
            
            if (i + 1) % 100 == 0:
                logger.info(f"Processed {i + 1}/{total} reviews")
        
        # Add results to dataframe
        df = df.copy()
        df['sentiment_label'] = sentiment_labels
        df['sentiment_score'] = sentiment_scores
        df['sentiment_category'] = sentiment_categories
        
        logger.info("✅ Sentiment analysis completed")
        return df
    
    def save_results(self, df):
        """Save sentiment analysis results"""
        df.to_csv(TASK2_PATHS['sentiment_results'], index=False)
        logger.info(f"💾 Sentiment results saved to: {TASK2_PATHS['sentiment_results']}")
        
        # Generate sentiment summary
        summary = df['sentiment_category'].value_counts()
        logger.info(f"📊 Sentiment Distribution: {summary.to_dict()}")
        
        return summary

def run_sentiment_analysis():
    """Main function to run sentiment analysis"""
    print("=" * 60)
    print("🎯 TASK 2: SENTIMENT ANALYSIS - FIXED VERSION")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = SentimentAnalyzer()
    
    # Load model
    if not analyzer.load_model():
        print("❌ Failed to load sentiment model")
        return False
    
    # Load data
    try:
        df = pd.read_csv(TASK2_PATHS['input_data'])
        print(f"✅ Loaded {len(df)} processed reviews")
    except FileNotFoundError:
        print("❌ Processed data not found. Run preprocessor.py first")
        return False
    
    # Analyze sentiment
    df_with_sentiment = analyzer.analyze_reviews_simple(df)
    
    if not df_with_sentiment.empty:
        summary = analyzer.save_results(df_with_sentiment)
        
        print("\n📊 SENTIMENT ANALYSIS RESULTS:")
        print("=" * 40)
        total = len(df_with_sentiment)
        for sentiment, count in summary.items():
            percentage = (count / total) * 100
            print(f"  {sentiment.upper()}: {count} reviews ({percentage:.1f}%)")
        
        return True
    else:
        print("❌ No results from sentiment analysis")
        return False

if __name__ == "__main__":
    run_sentiment_analysis()