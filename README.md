# 🚀 Social Media Trend Detection System

A modular trend detection platform that collects posts from **Instagram** and **Reddit**, processes them using **Natural Language Processing (NLP)**, and identifies trending topics based on engagement, freshness, and discussion patterns.

---

## ✨ Features

- 📸 Instagram data ingestion
- 👽 Reddit data ingestion
- 🧹 Data validation pipeline
- 🗄️ SQLite database using SQLAlchemy
- 🧠 NLP-based topic extraction
- 🤖 LLM-assisted canonical topic generation
- 📌 Automatic topic assignment
- 📈 Trend score calculation
- 📊 Interactive Streamlit dashboard

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
├── dashboard/
├── scripts/
├── src/
│   ├── ai/
│   ├── config/
│   ├── db/
│   ├── ingestion/
│   ├── nlp/
│   ├── scraper/
│   └── trends/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone <repository-url>
cd trend-detection
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```env
SCRAPFLY_API_KEY=your_scrapfly_api_key
OPENAI_API_KEY=your_openai_api_key
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

### Dashboard

```bash
streamlit run Home.py
```

---

## 🧠 NLP Pipeline

Each post passes through the following stages:

```text
Caption
   │
   ▼
Entity Extraction
   │
   ▼
Keyword Extraction
   │
   ▼
Candidate Generation
   │
   ▼
Canonical Topic Generation
   │
   ▼
Topic Validation
   │
   ▼
Topic Assignment
```

---

## 📈 Trend Score Calculation

The final trend score combines four independent metrics:

| Metric | Purpose |
|---------|---------|
| Engagement | Likes, comments, views |
| Freshness | Recency of posts |
| Velocity | Posting activity |
| Diversity | Number of unique contributors |

**Final Score**

```text
0.45 × Engagement
+ 0.30 × Freshness
+ 0.15 × Velocity
+ 0.10 × Diversity
```

---

## 📊 Dashboard

The Streamlit dashboard provides:

- Pipeline Control
- Dashboard Statistics
- Topics
- Trends
- Posts
- Accounts
- Analytics

---

## 🔧 Configuration

Instagram accounts:

```
src/config/seed_accounts.json
```

Reddit communities:

```
src/config/seed_subreddits.json
```

---

## 🚀 Future Improvements

- Twitter/X integration
- Sentiment Analysis
- Topic clustering
- REST API
- Real-time streaming
- Additional social media platforms

---

## 👨‍💻 Tech Stack

- Python
- Streamlit
- SQLAlchemy
- SQLite
- ScrapFly
- OpenAI API
- NLP

---

## 📄 License

This project was developed as part of an internship for educational and research purposes.