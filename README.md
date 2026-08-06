# 🚀 Social Media Trend Detection System

The Social Media Trend Detection System is a Python-based project that collects posts from Instagram and Reddit, processes them using Natural Language Processing (NLP), and identifies trending topics using engagement, freshness, velocity, and diversity metrics.

---

## ✨ Features

- Instagram post scraping using ScrapFly
- Reddit post scraping from configurable subreddits
- Unified data ingestion pipeline
- Data validation and quality checks
- SQLite storage using SQLAlchemy
- Entity extraction and keyword extraction
- AI-assisted canonical topic generation
- Topic assignment and trend scoring
- Interactive Streamlit dashboard

---

## 🏗️ Architecture

```text
                 Instagram
                      │
                      │
                 Reddit
                      │
                      ▼
              Data Ingestion
                      │
                      ▼
                 Validation
                      │
                      ▼
                 Database
                      │
                      ▼
               NLP Pipeline
                      │
                      ▼
             Topic Assignment
                      │
                      ▼
            Trend Score Engine
                      │
                      ▼
             Streamlit Dashboard
```

---

## 📂 Project Structure

```text
trend-detection/
│
├── docs/
├── infra/
├── scripts/
├── src/
│   ├── ai/
│   ├── config/
│   ├── db/
│   ├── ingestion/
│   ├── nlp/
│   ├── scraper/
│   ├── trends/
│   └── ui/
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/ananyasethi1907/trend-detection-system.git
cd trend-detection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file with your API keys:

```env
SCRAPFLY_API_KEY=your_scrapfly_api_key
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Running the Project

### Instagram Ingestion

```bash
python -m scripts.run_ingestion
```

### Reddit Ingestion

```bash
python -m scripts.run_reddit_ingestion
```

### NLP Pipeline

```bash
python -m scripts.run_nlp
```

### Trend Calculation

```bash
python -m scripts.calculate_trends
```

### Streamlit Dashboard

```bash
python -m streamlit run ui/app.py
```

> Replace `ui/app.py` with your application entry file if different.

---

## 🔧 Configuration

Instagram accounts:

```text
src/config/seed_accounts.json
```

Reddit communities:

```text
src/config/seed_subreddits.json
```

---

## 🧠 Data Pipeline

1. Data Collection
   - Instagram accounts
   - Reddit subreddits
2. Validation
   - Required fields
   - Timestamp validity
   - Engagement and platform-specific checks
3. Storage
   - Accounts
   - Posts
   - Topics
   - Trend scores
4. NLP Pipeline
   - Entity extraction
   - Keyword extraction
   - Candidate generation
   - Canonical topic generation
   - Topic validation
   - Topic assignment

---

## 📈 Trend Score Calculation

The final trend score is built from four metrics:

- Engagement: likes, comments, views, shares, saves
- Freshness: recency of posts
- Velocity: rate of discussion growth
- Diversity: contributions from unique sources

---

## 👨‍💻 Tech Stack

- Python
- Streamlit
- SQLAlchemy
- SQLite
- ScrapFly
- GRO API
- NLP

---

## 📄 License

This project is developed for educational and research purposes.
