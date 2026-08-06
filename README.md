Social Media Trend Detection System
Overview

The Social Media Trend Detection System is a Python-based application that identifies emerging trends by collecting data from multiple social media platforms, processing the content using Natural Language Processing (NLP), and calculating trend scores based on user engagement and content freshness.

The system currently supports:

Instagram
Reddit

Both platforms feed into a common processing pipeline, allowing trends to be analyzed using a unified architecture.

Features
Instagram post scraping using ScrapFly
Reddit post scraping from configurable subreddits
Unified data ingestion pipeline
Data validation
SQLite database storage using SQLAlchemy
Entity extraction
Keyword extraction
AI-assisted canonical topic generation
Topic assignment
Trend score calculation
Interactive Streamlit dashboard


Project Architecture
+--------------------+
|  Instagram Scraper |
+--------------------+
          |
          |
+--------------------+
|    Reddit Scraper   |
+--------------------+
          |
          ▼
+----------------------+
|  Data Ingestion Layer |
+----------------------+
          |
          ▼
+----------------------+
|      Validation      |
+----------------------+
          |
          ▼
+----------------------+
|    Database Storage  |
+----------------------+
          |
          ▼
+----------------------+
|     NLP Pipeline     |
+----------------------+
          |
          ▼
+----------------------+
| Topic Assignment     |
+----------------------+
          |
          ▼
+----------------------+
| Trend Score Engine   |
+----------------------+
          |
          ▼
+----------------------+
| Streamlit Dashboard  |
+----------------------+


Technology Stack
Backend
Python 3.x
SQLAlchemy
SQLite
NLP
Entity Extraction
Keyword Extraction
LLM-assisted Canonical Topic Generation
Data Collection
ScrapFly
Instagram Web API
Reddit HTML Parsing
Dashboard
Streamlit


Project Structure
trend-detection/

│
├── scripts/
│   ├── run_ingestion.py
│   ├── run_reddit_ingestion.py
│   ├── run_nlp.py
│   ├── calculate_trends.py
│   └── reset_topics.py
│
├── src/
│
│   ├── scraper/
│   │     ├── instagram.py
│   │     └── reddit.py
│   │
│   ├── ingestion/
│   │     ├── storage.py
│   │     └── validator.py
│   │
│   ├── nlp/
│   │     ├── entity_extractor.py
│   │     ├── keyword_extractor.py
│   │     ├── candidate_generator.py
│   │     ├── canonical_selector.py
│   │     ├── topic_generator.py
│   │     └── topic_assignment.py
│   │
│   ├── trends/
│   │     ├── engagement_score.py
│   │     ├── freshness_score.py
│   │     ├── velocity_score.py
│   │     ├── diversity_score.py
│   │     └── topic_trend_score_engine.py
│   │
│   ├── db/
│   │     ├── models.py
│   │     └── connection.py
│   │
│   ├── config/
│   │     ├── scoring_config.json
│   │     ├── seed_accounts.json
│   │     └── seed_subreddits.json
│   │
│   └── ai/
│         └── llm_canonical_resolver.py
│
├── dashboard/
│
└── README.md


Installation

Clone the repository

git clone <repository_url>

Navigate into the project

cd trend-detection

Install dependencies

pip install -r requirements.txt
Environment Variables

Create a .env file.

Example:

SCRAPFLY_API_KEY=your_scrapfly_api_key
OPENAI_API_KEY=your_openai_api_key
Configuration
Instagram Accounts

Located in

src/config/seed_accounts.json

Example

{
    "accounts": [
        "pagesix",
        "the.estd"
    ]
}
Reddit Communities

Located in

src/config/seed_subreddits.json

Example

{
    "subreddits": [
        "technology",
        "MachineLearning",
        "news",
        "india"
    ]
}


Running the Project
Instagram Ingestion
python -m scripts.run_ingestion
Reddit Ingestion
python -m scripts.run_reddit_ingestion
NLP Pipeline
python -m scripts.run_nlp
Trend Calculation
python -m scripts.calculate_trends
Streamlit Dashboard
streamlit run Home.py

(Replace Home.py with your application's entry file if different.)

Data Pipeline
Step 1 – Data Collection

The system collects posts from:

Instagram accounts
Reddit subreddits
Step 2 – Validation

Each post is validated by checking:

Required fields
Timestamp validity
Time window
Engagement threshold
Platform-specific quality checks
Step 3 – Database Storage

Validated posts are stored in:

Accounts
Posts

Topic information is later stored in:

Topics
PostTopicMap
TrendScores
Step 4 – NLP Pipeline

Each caption is processed through:

Caption

↓

Entity Extraction

↓

Keyword Extraction

↓

Candidate Generation

↓

Canonical Topic Selection (LLM + Rule-based)

↓

Topic Validation

↓

Topic Assignment
Trend Score Calculation

Each topic is assigned a trend score using four independent metrics.

Engagement

Measures popularity based on:

Likes
Comments
Views
Shares
Saves
Freshness

Measures recency of activity.

Recent posts receive higher freshness scores.

Velocity

Measures how rapidly discussion around a topic is growing.

Diversity

Measures discussion spread across:

Multiple accounts
Different posts
Metadata diversity
Final Formula
Trend Score

=

0.45 × Engagement

+

0.30 × Freshness

+

0.15 × Velocity

+

0.10 × Diversity
Database Schema
Accounts

Stores account information.

Posts

Stores all Instagram and Reddit posts.

Topics

Stores canonical topics generated by the NLP pipeline.

PostTopicMap

Maps posts to their corresponding topics.

TrendScores

Stores calculated trend scores.

Dashboard

The Streamlit dashboard provides:

Pipeline Control
Dashboard Statistics
Topic Explorer
Trend Explorer
Account Explorer
Post Explorer
Analytics

Users can:

Run Instagram ingestion
Run Reddit ingestion
Execute the NLP pipeline
Calculate trend scores
Reset topics
Future Improvements
Support for Twitter/X integration
Additional social media platforms
Sentiment Analysis
Topic clustering
Automatic category classification
Trend forecasting
Real-time streaming ingestion
REST API support
Dashboard filtering by source and category
Contributors

Developed as part of an internship project focused on building a scalable social media trend detection platform using data ingestion, NLP, and trend analytics.

License

This project is intended for educational and internship purposes. License terms may be updated according to organizational requirements.