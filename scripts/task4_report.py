# scripts/task4_report.py
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Setup
plt.style.use('default')
sns.set_theme(style="whitegrid")

def get_db_connection():
    """Connect to PostgreSQL database"""
    return psycopg2.connect(
        host='localhost',
        database='bank_reviews',
        user='postgres',
        password='password'
    )

def generate_comprehensive_report():
    """Generate comprehensive Task 4 report"""
    print("📋 GENERATING COMPREHENSIVE TASK 4 REPORT")
    print("=" * 60)
    
    # Load data
    conn = get_db_connection()
    query = "SELECT r.*, b.bank_name FROM reviews r JOIN banks b ON r.bank_id = b.bank_id"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Create report directory
    os.makedirs('outputs/report', exist_ok=True)
    
    # Generate report content
    report_content = generate_report_content(df)
    
    # Save report to file
    report_path = 'outputs/report/task4_final_report.txt'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Comprehensive report saved to: {report_path}")
    return report_content

def generate_report_content(df):
    """Generate the report content"""
    report = []
    
    # Header
    report.append("FINANCIAL TECHNOLOGY REVIEWS ANALYSIS - TASK 4 REPORT")
    report.append("=" * 60)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total Reviews Analyzed: {len(df):,}")
    report.append("")
    
    # Executive Summary
    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 40)
    report.append("Analysis of 9,071 user reviews from three Ethiopian banks reveals")
    report.append("significant differences in mobile app satisfaction and performance.")
    report.append("")
    
    # Key Findings
    report.append("KEY FINDINGS")
    report.append("-" * 40)
    
    # Performance ranking
    bank_ratings = df.groupby('bank_name')['rating'].mean().sort_values(ascending=False)
    report.append("🏆 PERFORMANCE RANKING:")
    for i, (bank, rating) in enumerate(bank_ratings.items(), 1):
        report.append(f"  {i}. {bank}: {rating:.2f}/5")
    report.append("")
    
    # Critical insights
    report.append("📊 CRITICAL INSIGHTS:")
    report.append(f"  • Dashen Bank leads with {bank_ratings.iloc[0]:.2f}/5 rating")
    report.append(f"  • Bank of Abyssinia trails with {bank_ratings.iloc[-1]:.2f}/5 rating")
    report.append(f"  • {df[df['rating'] == 5].shape[0]:,} 5-star reviews ({df[df['rating'] == 5].shape[0]/len(df)*100:.1f}%)")
    report.append(f"  • {df[df['rating'] == 1].shape[0]:,} 1-star reviews ({df[df['rating'] == 1].shape[0]/len(df)*100:.1f}%)")
    report.append("")
    
    # Detailed Bank Analysis
    report.append("DETAILED BANK ANALYSIS")
    report.append("-" * 40)
    
    for bank in df['bank_name'].unique():
        bank_data = df[df['bank_name'] == bank]
        avg_rating = bank_data['rating'].mean()
        
        report.append(f"\n🏦 {bank.upper()}")
        report.append(f"  Overall Rating: {avg_rating:.2f}/5")
        report.append(f"  Total Reviews: {len(bank_data):,}")
        
        # Rating distribution
        rating_counts = bank_data['rating'].value_counts().sort_index()
        report.append("  Rating Distribution:")
        for rating in range(1, 6):
            count = rating_counts.get(rating, 0)
            percentage = (count / len(bank_data)) * 100
            stars = "⭐" * rating
            report.append(f"    {stars} {rating}-star: {count:,} ({percentage:.1f}%)")
    
    # Recommendations
    report.append("\n🎯 STRATEGIC RECOMMENDATIONS")
    report.append("-" * 40)
    
    # Dashen Bank (Best performer)
    report.append("\n🏆 DASHEN BANK - CAPITALIZE ON SUCCESS:")
    report.append("  • Maintain current app performance and user experience")
    report.append("  • Leverage high ratings in marketing campaigns")
    report.append("  • Continue gathering user feedback for incremental improvements")
    report.append("  • Consider expanding feature set while maintaining stability")
    
    # Commercial Bank of Ethiopia
    report.append("\n📈 COMMERCIAL BANK OF ETHIOPIA - ENHANCE PERFORMANCE:")
    report.append("  • Address common technical issues reported by users")
    report.append("  • Improve app loading speed and transaction processing")
    report.append("  • Enhance customer support responsiveness")
    report.append("  • Focus on reducing 1-star reviews (currently 20.4%)")
    
    # Bank of Abyssinia
    report.append("\n🚨 BANK OF ABYSSINIA - URGENT IMPROVEMENT NEEDED:")
    report.append("  • Immediate investigation into high 1-star review rate (47.6%)")
    report.append("  • Prioritize bug fixes and app stability")
    report.append("  • Implement user feedback system for rapid improvements")
    report.append("  • Consider major app redesign based on user complaints")
    report.append("  • Launch customer satisfaction recovery campaign")
    
    # Business Impact
    report.append("\n💼 BUSINESS IMPACT ASSESSMENT")
    report.append("-" * 40)
    report.append("Mobile app performance directly correlates with:")
    report.append("  • Customer retention and satisfaction")
    report.append("  • Brand reputation and trust")
    report.append("  • Competitive positioning in fintech market")
    report.append("  • Potential impact on customer acquisition costs")
    report.append("")
    report.append("Improving app ratings by 1 star could significantly impact:")
    report.append("  • User retention rates")
    report.append("  • Positive word-of-mouth marketing")
    report.append("  • Reduced customer support costs")
    
    # Next Steps
    report.append("\n🔄 RECOMMENDED NEXT STEPS")
    report.append("-" * 40)
    report.append("1. Conduct detailed thematic analysis of review content")
    report.append("2. Implement A/B testing for app improvements")
    report.append("3. Establish continuous monitoring of app store reviews")
    report.append("4. Develop targeted improvement roadmaps for each bank")
    report.append("5. Schedule quarterly performance reviews")
    
    report.append("\n" + "=" * 60)
    report.append("END OF REPORT")
    report.append("=" * 60)
    
    return "\n".join(report)

def create_dashboard_visualizations(df):
    """Create additional visualizations for the report"""
    print("\n🎨 Creating dashboard visualizations...")
    
    # 1. Performance comparison
    plt.figure(figsize=(12, 8))
    
    # Subplot 1: Average ratings
    plt.subplot(2, 2, 1)
    avg_ratings = df.groupby('bank_name')['rating'].mean().sort_values(ascending=False)
    bars = plt.bar(avg_ratings.index, avg_ratings.values, color=['#27ae60', '#f39c12', '#e74c3c'])
    plt.title('Average Rating by Bank', fontweight='bold')
    plt.ylabel('Rating (1-5 stars)')
    plt.xticks(rotation=45)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height, f'{height:.2f}', 
                ha='center', va='bottom', fontweight='bold')
    
    # Subplot 2: Review distribution
    plt.subplot(2, 2, 2)
    review_counts = df['bank_name'].value_counts()
    plt.pie(review_counts.values, labels=review_counts.index, autopct='%1.1f%%')
    plt.title('Review Distribution by Bank', fontweight='bold')
    
    # Subplot 3: Rating distribution
    plt.subplot(2, 2, 3)
    rating_dist = df['rating'].value_counts().sort_index()
    plt.bar(rating_dist.index, rating_dist.values, color='skyblue')
    plt.title('Overall Rating Distribution', fontweight='bold')
    plt.xlabel('Rating')
    plt.ylabel('Number of Reviews')
    
    # Subplot 4: Sentiment analysis
    plt.subplot(2, 2, 4)
    sentiment_dist = df['sentiment_label'].str.upper().value_counts()
    colors = ['#2ecc71', '#e74c3c', '#f39c12']
    plt.pie(sentiment_dist.values, labels=sentiment_dist.index, autopct='%1.1f%%', colors=colors)
    plt.title('Overall Sentiment Distribution', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/report/performance_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Dashboard visualization saved to outputs/report/performance_dashboard.png")

def main():
    """Main report generation function"""
    print("🚀 TASK 4 - COMPREHENSIVE REPORT GENERATION")
    print("=" * 60)
    
    # Generate comprehensive report
    report = generate_comprehensive_report()
    
    # Create dashboard visualizations
    create_dashboard_visualizations(pd.read_sql_query(
        "SELECT r.*, b.bank_name FROM reviews r JOIN banks b ON r.bank_id = b.bank_id",
        get_db_connection()
    ))
    
    print("\n" + "=" * 60)
    print("🎉 TASK 4 REPORT GENERATION COMPLETED!")
    print("📄 Report: outputs/report/task4_final_report.txt")
    print("📊 Dashboard: outputs/report/performance_dashboard.png")
    print("💼 Ready for stakeholder presentation!")

if __name__ == "__main__":
    main()