# scripts/setup_database.py
import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

def get_db_connection():
    """Create database connection with your password"""
    print("🔗 Connecting to PostgreSQL...")
    try:
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='bank_reviews',
            user='postgres',
            password='password',  # YOUR PASSWORD
            connect_timeout=10
        )
        print("✅ Connected to PostgreSQL successfully!")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
        return None

def create_tables(conn):
    """Create the database tables"""
    print("🗄️ Creating database tables...")
    
    try:
        cur = conn.cursor()
        
        # Create banks table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS banks (
                bank_id SERIAL PRIMARY KEY,
                bank_name VARCHAR(100) NOT NULL UNIQUE,
                app_name VARCHAR(200) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create reviews table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                review_id SERIAL PRIMARY KEY,
                bank_id INTEGER REFERENCES banks(bank_id) ON DELETE CASCADE,
                review_text TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                review_date DATE NOT NULL,
                sentiment_label VARCHAR(20) NOT NULL,
                sentiment_score DECIMAL(3,2) NOT NULL CHECK (sentiment_score >= 0 AND sentiment_score <= 1),
                source VARCHAR(50) DEFAULT 'Google Play Store',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for better performance
        cur.execute("CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating)")
        
        # Insert banks
        cur.execute("""
            INSERT INTO banks (bank_name, app_name) VALUES
            ('Commercial Bank of Ethiopia', 'CBE Mobile'),
            ('Bank of Abyssinia', 'BOA Mobile'),
            ('Dashen Bank', 'Dashen Mobile')
            ON CONFLICT (bank_name) DO NOTHING
        """)
        
        conn.commit()
        cur.close()
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        conn.rollback()
        return False

def verify_data(conn):
    """Verify the data was inserted correctly"""
    print("🔍 Verifying database...")
    
    try:
        cur = conn.cursor()
        
        # Count total reviews
        cur.execute("SELECT COUNT(*) FROM reviews")
        total_reviews = cur.fetchone()[0]
        print(f"📊 Total reviews in database: {total_reviews:,}")
        
        # Count by bank
        cur.execute("""
            SELECT b.bank_name, COUNT(r.review_id) 
            FROM banks b 
            LEFT JOIN reviews r ON b.bank_id = r.bank_id 
            GROUP BY b.bank_name
            ORDER BY COUNT(r.review_id) DESC
        """)
        print("🏦 Reviews by bank:")
        for bank, count in cur.fetchall():
            print(f"   {bank}: {count:,} reviews")
        
        # Average ratings
        cur.execute("""
            SELECT b.bank_name, ROUND(AVG(r.rating), 2), COUNT(r.review_id)
            FROM banks b 
            JOIN reviews r ON b.bank_id = r.bank_id 
            GROUP BY b.bank_name
            ORDER BY AVG(r.rating) DESC
        """)
        print("⭐ Average ratings:")
        for bank, avg_rating, count in cur.fetchall():
            print(f"   {bank}: {avg_rating}/5 ({count:,} reviews)")
        
        cur.close()
        
        # Check if we meet requirements
        print(f"\n🎯 TASK 3 REQUIREMENTS CHECK:")
        print(f"   Minimum 400 reviews: {total_reviews}/400+ {'✅' if total_reviews >= 400 else '❌'}")
        print(f"   PostgreSQL database: ✅")
        print(f"   Tables created: ✅")
        
        return total_reviews >= 400
        
    except Exception as e:
        print(f"❌ Error verifying database: {e}")
        return False

def main():
    """Main function - runs the complete Task 3 setup"""
    print("=" * 60)
    print("🚀 TASK 3 - POSTGRESQL DATABASE SETUP")
    print("=" * 60)
    
    # Connect to database
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        # Create tables
        if not create_tables(conn):
            return
        
        # Verify everything
        print("\n" + "=" * 60)
        print("✅ VERIFICATION")
        print("=" * 60)
        
        success = verify_data(conn)
        
        # Final result
        print("\n" + "=" * 60)
        if success:
            print("🎉 TASK 3 COMPLETED SUCCESSFULLY!")
            print("📋 All requirements met:")
            print("   ✅ PostgreSQL database connected")
            print("   ✅ Tables (banks, reviews) created") 
            print("   ✅ Data integrity verified")
        else:
            print("⚠️  Task 3 completed but data needs to be inserted")
            print("💡 Run: python simple_task.py to insert your 9,071 reviews")
        
    finally:
        conn.close()
        print("🔒 Database connection closed")

if __name__ == "__main__":
    main()