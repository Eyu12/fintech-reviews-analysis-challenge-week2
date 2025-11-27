"""
Task 2: Thematic Analysis - Find common topics in reviews
"""
import pandas as pd
import numpy as np
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import re
from task2_config import THEMATIC_CONFIG, TASK2_PATHS

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ThematicAnalyzer:
    def __init__(self):
        self.config = THEMATIC_CONFIG
        self.theme_keywords = self.config['theme_keywords']
    
    def load_data(self):
        """Load data with sentiment analysis"""
        try:
            df = pd.read_csv(TASK2_PATHS['sentiment_results'])
            logger.info(f"✅ Loaded {len(df)} reviews with sentiment")
            return df
        except FileNotFoundError:
            logger.error("❌ Sentiment data not found. Run sentiment_analysis.py first")
            return None
    
    def extract_keywords_tfidf(self, texts, top_n=20):
        """Extract important keywords using TF-IDF"""
        try:
            vectorizer = TfidfVectorizer(
                max_features=self.config['tfidf_max_features'],
                stop_words='english',
                ngram_range=(1, 2)  # Single words and two-word phrases
            )
            
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.sum(axis=0).A1
            
            keywords_df = pd.DataFrame({
                'keyword': feature_names,
                'tfidf_score': tfidf_scores
            }).sort_values('tfidf_score', ascending=False)
            
            return keywords_df.head(top_n)
        except Exception as e:
            logger.error(f"Error in TF-IDF: {e}")
            return pd.DataFrame()
    
    def assign_themes_to_reviews(self, review_text, keywords_df):
        """Assign themes to a review based on keyword matching"""
        if pd.isna(review_text):
            return []
        
        review_text_lower = str(review_text).lower()
        assigned_themes = []
        
        for theme, keywords in self.theme_keywords.items():
            # Check if any theme keyword appears in the review
            theme_keywords_found = []
            for keyword in keywords:
                if keyword in review_text_lower:
                    theme_keywords_found.append(keyword)
            
            # Assign theme if enough keywords found
            if len(theme_keywords_found) >= 1:  # At least 1 keyword match
                assigned_themes.append(theme)
        
        return assigned_themes
    
    def analyze_themes_by_bank(self, df):
        """Analyze themes for each bank separately"""
        logger.info("🔍 Starting thematic analysis by bank...")
        
        banks = df['bank'].unique()
        all_themes_data = []
        
        for bank in banks:
            logger.info(f"Analyzing themes for {bank}...")
            bank_reviews = df[df['bank'] == bank]
            
            if len(bank_reviews) < 10:  # Skip if too few reviews
                continue
            
            # Extract keywords for this bank
            bank_texts = bank_reviews['cleaned_review'].dropna().tolist()
            keywords_df = self.extract_keywords_tfidf(bank_texts)
            
            if not keywords_df.empty:
                logger.info(f"Top keywords for {bank}: {list(keywords_df['keyword'].head(5))}")
            
            # Assign themes to each review
            for idx, row in bank_reviews.iterrows():
                themes = self.assign_themes_to_reviews(row['cleaned_review'], keywords_df)
                
                for theme in themes:
                    all_themes_data.append({
                        'review_id': row.get('review_id', idx),
                        'bank': bank,
                        'rating': row['rating'],
                        'sentiment_category': row.get('sentiment_category', 'unknown'),
                        'theme': theme,
                        'review_text': row['cleaned_review'][:100] + '...' if len(row['cleaned_review']) > 100 else row['cleaned_review']
                    })
        
        themes_df = pd.DataFrame(all_themes_data)
        logger.info("✅ Thematic analysis completed")
        return themes_df
    
    def generate_theme_summary(self, themes_df):
        """Generate summary of themes by bank and sentiment"""
        if themes_df.empty:
            return pd.DataFrame()
        
        # Summary by bank and theme
        theme_summary = themes_df.groupby(['bank', 'theme']).size().reset_index(name='count')
        theme_summary = theme_summary.sort_values(['bank', 'count'], ascending=[True, False])
        
        # Summary by theme and sentiment
        sentiment_summary = themes_df.groupby(['theme', 'sentiment_category']).size().reset_index(name='count')
        sentiment_summary = sentiment_summary.sort_values(['theme', 'count'], ascending=[True, False])
        
        return {
            'by_bank': theme_summary,
            'by_sentiment': sentiment_summary
        }
    
    def save_results(self, themes_df, summary):
        """Save thematic analysis results"""
        # Save detailed themes data
        themes_df.to_csv(TASK2_PATHS['thematic_results'], index=False)
        logger.info(f"💾 Thematic results saved to: {TASK2_PATHS['thematic_results']}")
        
        # Save summary
        if not summary['by_bank'].empty:
            summary['by_bank'].to_csv('data/results/theme_summary_by_bank.csv', index=False)
            logger.info("💾 Theme summary by bank saved")
        
        if not summary['by_sentiment'].empty:
            summary['by_sentiment'].to_csv('data/results/theme_summary_by_sentiment.csv', index=False)
            logger.info("💾 Theme summary by sentiment saved")
        
        return summary

def run_thematic_analysis():
    """Main function to run thematic analysis"""
    print("=" * 60)
    print("🎯 TASK 2: THEMATIC ANALYSIS")
    print("=" * 60)
    
    # Initialize analyzer
    analyzer = ThematicAnalyzer()
    
    # Load data
    df = analyzer.load_data()
    if df is None:
        return False
    
    # Analyze themes
    themes_df = analyzer.analyze_themes_by_bank(df)
    
    if not themes_df.empty:
        # Generate summary
        summary = analyzer.generate_theme_summary(themes_df)
        
        # Save results
        analyzer.save_results(themes_df, summary)
        
        print("\n📊 THEMATIC ANALYSIS RESULTS:")
        print("=" * 40)
        
        # Show top themes by bank
        bank_summary = summary['by_bank']
        for bank in bank_summary['bank'].unique():
            bank_themes = bank_summary[bank_summary['bank'] == bank].head(3)
            print(f"\n🏦 {bank.upper()} - Top Themes:")
            for _, theme_row in bank_themes.iterrows():
                print(f"   • {theme_row['theme']}: {theme_row['count']} mentions")
        
        # Show overall theme distribution
        print(f"\n📈 Overall Themes Found: {len(themes_df['theme'].unique())}")
        print(f"📝 Total Theme Mentions: {len(themes_df)}")
        
        return True
    else:
        print("❌ No themes found in the analysis")
        return False

if __name__ == "__main__":
    run_thematic_analysis()