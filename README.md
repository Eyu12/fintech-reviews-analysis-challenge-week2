# Ethiopian Mobile Banking App Review Analysis

## Overview

This repository contains a comprehensive analysis of Google Play Store reviews for three Ethiopian mobile banking applications:

- **Commercial Bank of Ethiopia (CBE)**
- **Bank of Abyssinia (BOA)**
- **Dashen Bank**

The project was conducted as part of the **10 Academy Week 2 Challenge** and covers **Tasks 1–4**, including data collection, cleaning, storage, analysis, visualization, and actionable business insights.

---

## Table of Contents

1. [Project Objectives](#project-objectives)  
2. [Tasks Overview](#tasks-overview)  
3. [Data Description](#data-description)  
4. [Repository Structure](#repository-structure)  
5. [Setup and Requirements](#setup-and-requirements)  
6. [Database Details (Task 3)](#database-details-task-3)  
7. [Analysis and Insights (Task 4)](#analysis-and-insights-task-4)  
8. [Results and Recommendations](#results-and-recommendations)  
9. [Visualization](#visualization)  
10. [Contributing](#contributing)  
11. [License](#license)

---

## Project Objectives

- Evaluate user experiences across CBE, BOA, and Dashen mobile apps.  
- Identify **key satisfaction drivers** and **pain points**.  
- Store cleaned review data in a robust PostgreSQL database.  
- Conduct sentiment analysis and extract actionable insights.  
- Provide **recommendations** to improve user satisfaction and app performance.

---

## Tasks Overview

### **Task 1: Data Collection**
- Scraped Google Play Store reviews for all three banking apps.  
- Collected over **7,000 reviews** including text, rating, date, and source.

### **Task 2: Data Cleaning & Preprocessing**
- Removed duplicates and spam.  
- Normalized text, tokenized, and removed stopwords.  
- Added **sentiment labels** and **scores**.  
- Extracted keywords for theme analysis.

### **Task 3: Database Implementation**
- PostgreSQL database `bank_reviews` created with two tables:
  - **banks**: bank_id, bank_name, app_name  
  - **reviews**: review_id, bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, source  
- Indexed key columns for **performance**.  
- Ensured **data integrity** with foreign keys, checks, and unique constraints.  
- Inserted **9,071 reviews** using Python (SQLAlchemy/psycopg2).

### **Task 4: Insights & Recommendations**
- Sentiment analysis across all reviews.  
- Identified **drivers** (fast transactions, user-friendly interface) and **pain points** (crashes, login issues).  
- Benchmarked bank performance:
  - Dashen Bank: 4.07/5 (leader)  
  - CBE: 3.72/5  
  - BOA: 2.73/5 (requires urgent improvement)  
- Provided actionable recommendations for each bank.  
- Visualized trends, rating distributions, sentiment patterns, and keyword frequencies.

---

## Data Description

| Field | Description |
|-------|-------------|
| review_id | Unique identifier for each review |
| bank_id | Foreign key linking to the banks table |
| review_text | User review text |
| rating | Star rating (1–5) |
| review_date | Date of review |
| sentiment_label | Positive / Neutral / Negative |
| sentiment_score | Numeric sentiment score |
| source | Review platform (Google Play) |

---

## Repository Structure

```bash
FINTECH-REVIEWS-ANALYSIS-CHALLENGE-WEEK2/
├── .github/workflows/
├── data/
│   ├── processed/
│   ├── raw/
│   └── results/
├── logs/
├── notebooks/
│   ├── preprocessing.ipynb
│   └── task2_analysis.ipynb
├── outputs/
│   ├── report/
│   └── visuals/
├── scripts/
│   ├── __pycache__/
│   ├── config.py
│   ├── setup_database.py
│   ├── preprocessor.py
│   ├── scraper.py
│   ├── sentiment_analysis.py
│   ├── task2_config.py
│   ├── task4_analysis.py
│   ├── task4_report.py
│   └── thematic_analysis.py
├── .venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt

## Setup and Requirements

### **Python Libraries**
- pandas, numpy, matplotlib, seaborn  
- SQLAlchemy, psycopg2  
- nltk

### **PostgreSQL**
- Version 13+ recommended  
- Database: `bank_reviews`  
- Run `sql/schema.sql` to create tables and indexes

### **Usage**

# Clone repository
git clone 

# Install Python dependencies
pip install -r requirements.txt

## Data Collection (Task 1)
- Scraped Google Play Store reviews for CBE, BOA, and Dashen Bank apps.
- Collected key metadata:
 - review_text
 - rating (1–5 stars)
 - review_date
 - source (Google Play)
- Collected a total of over 7,000 reviews, representing a comprehensive dataset of user feedback.
- Ensured initial data quality by removing incomplete entries during scraping.

## Data Cleaning & Preprocessing (Task 2)
- Removed duplicates, spam, and irrelevant reviews.
- Standardized text: lowercasing, punctuation removal, and tokenization.
- Removed stopwords and performed keyword extraction for thematic analysis.
- Applied sentiment analysis to generate:
 - sentiment_label (Positive, Neutral, Negative)
 - sentiment_score (numeric value)
- Prepared data for storage in PostgreSQL, ensuring consistency and usability for analysis

## Database Details (Task 3)
- Tables: banks, reviews
- Review count: 9,071
- Completeness: 99.8%
- Query performance: Sub-second
- Integrity: Foreign key, check, and unique constraints enforced
- Scalability: Supports >100,000 reviews

## Analysis and Insights (Task 4)
- Top Drivers: Fast transactions, reliability, intuitive interface
- Pain Points: App crashes, login issues, slow response
- Bank Performance:
 - Dashen: Leading in satisfaction
 - CBE: Moderate, mixed feedback
 - BOA: Urgent improvement required
- Recommendations:
 - Dashen: Maintain stability and incremental improvements
 - CBE: Optimize performance and support
 - BOA: Bug fixes, redesign, customer recovery campaigns
