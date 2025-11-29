-- Database schema for bank reviews
CREATE TABLE IF NOT EXISTS banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL UNIQUE,
    app_name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

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
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_reviews_bank_id ON reviews(bank_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_reviews_sentiment ON reviews(sentiment_label);
CREATE INDEX IF NOT EXISTS idx_reviews_date ON reviews(review_date);

-- Insert initial bank data
INSERT INTO banks (bank_name, app_name) VALUES
('Commercial Bank of Ethiopia', 'CBE Mobile'),
('Bank of Abyssinia', 'BOA Mobile'),
('Dashen Bank', 'Dashen Mobile')
ON CONFLICT (bank_name) DO NOTHING;