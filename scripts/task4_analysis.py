# scripts/task4_analysis.py
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import os

# Setup - FIXED STYLING
load_dotenv()
plt.style.use('default')  # Use default style instead of seaborn
sns.set_theme(style="whitegrid")  # Updated seaborn style

def get_db_connection():
    """Connect to PostgreSQL database"""
    return psycopg2.connect(
        host='localhost',
        database='bank_reviews',
        user='postgres',
        password='password'
    )

def load_data_from_db():
    """Load review data from PostgreSQL"""
    print("📊 Loading data from PostgreSQL...")
    
    conn = get_db_connection()
    
    # Load all reviews with bank information
    query = """
    SELECT r.*, b.bank_name, b.app_name 
    FROM reviews r 
    JOIN banks b ON r.bank_id = b.bank_id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    print(f"✅ Loaded {len(df)} reviews from database")
    return df

def basic_analysis(df):
    """Perform basic data analysis"""
    print("\n" + "="*50)
    print("📈 BASIC ANALYSIS")
    print("="*50)
    
    # Overall statistics
    print(f"📊 Total Reviews: {len(df):,}")
    print(f"🏦 Banks: {df['bank_name'].unique().tolist()}")
    
    # Reviews per bank
    bank_counts = df['bank_name'].value_counts()
    print("\n🏦 Reviews per Bank:")
    for bank, count in bank_counts.items():
        print(f"   {bank}: {count:,} reviews")
    
    # Rating distribution
    print(f"\n⭐ Overall Average Rating: {df['rating'].mean():.2f}/5")
    
    # Ratings by bank
    print("\n⭐ Ratings by Bank:")
    ratings_by_bank = df.groupby('bank_name')['rating'].agg(['mean', 'count'])
    for bank, row in ratings_by_bank.iterrows():
        print(f"   {bank}: {row['mean']:.2f}/5 ({row['count']:,} reviews)")
    
    # Sentiment analysis
    print(f"\n😊 Sentiment Distribution:")
    sentiment_counts = df['sentiment_label'].value_counts()
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        print(f"   {sentiment}: {count:,} reviews ({percentage:.1f}%)")

def create_basic_visualizations(df):
    """Create basic charts and save them"""
    print("\n🎨 Creating visualizations...")
    
    # Create outputs directory
    os.makedirs('outputs/visuals', exist_ok=True)
    
    # 1. Rating distribution by bank
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x='bank_name', y='rating')
    plt.title('Rating Distribution by Bank', fontsize=14, fontweight='bold')
    plt.xlabel('Bank', fontsize=12)
    plt.ylabel('Rating (1-5 stars)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/visuals/ratings_by_bank.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Sentiment distribution
    plt.figure(figsize=(10, 6))
    sentiment_counts = df['sentiment_label'].value_counts()
    colors = ['#2ecc71', '#e74c3c', '#f39c12']  # Green, Red, Orange
    plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', colors=colors)
    plt.title('Overall Sentiment Distribution', fontsize=14, fontweight='bold')
    plt.savefig('outputs/visuals/sentiment_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Reviews per bank
    plt.figure(figsize=(10, 6))
    bank_counts = df['bank_name'].value_counts()
    bars = plt.bar(bank_counts.index, bank_counts.values, color=['#3498db', '#9b59b6', '#1abc9c'])
    plt.title('Number of Reviews per Bank', fontsize=14, fontweight='bold')
    plt.xlabel('Bank', fontsize=12)
    plt.ylabel('Number of Reviews', fontsize=12)
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('outputs/visuals/reviews_per_bank.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Average rating by bank
    plt.figure(figsize=(10, 6))
    avg_ratings = df.groupby('bank_name')['rating'].mean().sort_values(ascending=False)
    bars = plt.bar(avg_ratings.index, avg_ratings.values, color=['#27ae60', '#f39c12', '#e74c3c'])
    plt.title('Average Rating by Bank', fontsize=14, fontweight='bold')
    plt.xlabel('Bank', fontsize=12)
    plt.ylabel('Average Rating', fontsize=12)
    plt.ylim(0, 5)
    plt.xticks(rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('outputs/visuals/avg_rating_by_bank.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Visualizations saved to outputs/visuals/")

# scripts/task4_analysis.py - UPDATED SENTIMENT ANALYSIS
def generate_insights(df):
    """Generate business insights"""
    print("\n" + "="*50)
    print("💡 BUSINESS INSIGHTS")
    print("="*50)
    
    # Find best and worst performing banks
    bank_performance = df.groupby('bank_name').agg({
        'rating': 'mean',
        'sentiment_score': 'mean',
        'review_id': 'count'
    }).round(2)
    
    best_bank = bank_performance['rating'].idxmax()
    worst_bank = bank_performance['rating'].idxmin()
    
    print(f"🏆 Best Performing Bank: {best_bank} ({bank_performance.loc[best_bank, 'rating']}/5)")
    print(f"⚠️  Needs Improvement: {worst_bank} ({bank_performance.loc[worst_bank, 'rating']}/5)")
    
    # FIXED: Sentiment analysis by bank (handle case sensitivity)
    print(f"\n😊 Sentiment by Bank:")
    # Convert sentiment labels to consistent case
    df['sentiment_lower'] = df['sentiment_label'].str.lower()
    
    sentiment_by_bank = pd.crosstab(df['bank_name'], df['sentiment_lower'], normalize='index') * 100
    
    for bank in sentiment_by_bank.index:
        positives = sentiment_by_bank.loc[bank, 'positive'] if 'positive' in sentiment_by_bank.columns else 0
        negatives = sentiment_by_bank.loc[bank, 'negative'] if 'negative' in sentiment_by_bank.columns else 0
        neutrals = sentiment_by_bank.loc[bank, 'neutral'] if 'neutral' in sentiment_by_bank.columns else 0
        print(f"   {bank}: {positives:.1f}% positive, {negatives:.1f}% negative, {neutrals:.1f}% neutral")
    
    # Rating distribution insights
    print(f"\n⭐ Rating Insights:")
    for bank in df['bank_name'].unique():
        bank_data = df[df['bank_name'] == bank]
        avg_rating = bank_data['rating'].mean()
        five_star = (bank_data['rating'] == 5).sum()
        one_star = (bank_data['rating'] == 1).sum()
        
        print(f"   {bank}:")
        print(f"     • Average: {avg_rating:.2f}/5")
        print(f"     • 5-star reviews: {five_star:,} ({five_star/len(bank_data)*100:.1f}%)")
        print(f"     • 1-star reviews: {one_star:,} ({one_star/len(bank_data)*100:.1f}%)")

def generate_recommendations(df):
    """Generate actionable recommendations"""
    print("\n" + "="*50)
    print("🎯 ACTIONABLE RECOMMENDATIONS")
    print("="*50)
    
    # Analyze each bank's performance
    for bank in df['bank_name'].unique():
        bank_data = df[df['bank_name'] == bank]
        avg_rating = bank_data['rating'].mean()
        
        print(f"\n🏦 {bank} (Rating: {avg_rating:.2f}/5):")
        
        if avg_rating >= 4.0:
            print("   ✅ Strengths:")
            print("   • Maintain current app performance")
            print("   • Continue positive user experience")
            print("   • Leverage high ratings for marketing")
        elif avg_rating >= 3.0:
            print("   📈 Areas for Improvement:")
            print("   • Address common user complaints")
            print("   • Improve app stability and speed")
            print("   • Enhance customer support")
        else:
            print("   🚨 Critical Issues:")
            print("   • Urgent need for app improvements")
            print("   • Investigate frequent crashes/errors")
            print("   • Prioritize user feedback implementation")

def main():
    """Main Task 4 analysis function"""
    print("🚀 STARTING TASK 4 - INSIGHTS AND RECOMMENDATIONS")
    print("="*60)
    
    # Load data from PostgreSQL
    df = load_data_from_db()
    
    # Perform analysis
    basic_analysis(df)
    
    # Create visualizations
    create_basic_visualizations(df)
    
    # Generate insights
    generate_insights(df)
    
    # Generate recommendations
    generate_recommendations(df)
    
    print("\n" + "="*60)
    print("🎉 TASK 4 ANALYSIS COMPLETED!")
    print("📁 Outputs saved to: outputs/visuals/")
    print("📊 Generated: 4 visualizations + insights + recommendations")
    print("💡 Next: Create detailed report and advanced analysis")

if __name__ == "__main__":
    main()