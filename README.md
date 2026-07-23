# Instagram Trend Detection System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue" alt="Python 3.11+" />
  <img src="https://img.shields.io/badge/Streamlit-dashboard-ff4b4b" alt="Streamlit dashboard" />
  <img src="https://img.shields.io/badge/SQLAlchemy-ORM-orange" alt="SQLAlchemy ORM" />
  <img src="https://img.shields.io/badge/SQLite-local-db-lightgrey" alt="SQLite" />
</p>

A full-stack trend detection pipeline for Instagram content analysis, built to ingest posts, extract topics, score trends, and visualize insights through a Streamlit dashboard.

## Overview

This project ingests Instagram account content, validates and stores posts, performs NLP processing to generate topics, and computes trend scores that can be explored in the UI.

The repository combines:

- data ingestion and validation
- natural language processing
- topic assignment and scoring
- Streamlit-based monitoring and analysis dashboard
- database-backed persistence with SQLAlchemy

## Key Features

- Ingest posts from configured seed accounts
- Validate incoming content using configurable rules
- Extract entities, keywords, and topic labels
- Assign posts to topics for trend analysis
- Generate trend scores from topic/post activity
- Visualize results through the Streamlit UI

## Project Architecture

```text
┌─────────────────────┐
│   UI / Streamlit     │
│   ui/app.py          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Pipeline Scripts   │
│ scripts/run_ingestion│
│ scripts/run_nlp.py   │
│ scripts/calculate_   │
│ trends.py            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Core Source Modules │
│  src/ingestion       │
│  src/nlp             │
│  src/trends          │
│  src/scoring         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    SQLite DB         │
│  trend_detection.db  │
└─────────────────────┘
```

## Main Workflow

Run the pipeline in this order:

1. `run_ingestion.py`
2. `run_nlp.py`
3. `calculate_trends.py`
4. optionally run `reset_nlp_data.py` to clear generated NLP state

## Project Structure

```text
.
├── docs/                    # product and operational documentation
├── scripts/                 # pipeline and maintenance scripts
├── src/                     # application source code
├── ui/                      # Streamlit dashboard UI
├── scoring_config.json      # scoring configuration
├── create_tables.py         # database table bootstrap helper
└── README.md                # project overview
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/ananyasethi1907/trend-detection-system.git
cd trend-detection-system
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If a requirements file is not present, install the project dependencies manually using your current environment setup.

### 4. Initialize the database

```bash
python create_tables.py
```

## Running the Pipeline

### Run ingestion

```bash
python -m scripts.run_ingestion
```

### Run NLP pipeline

```bash
python -m scripts.run_nlp
```

### Calculate trends

```bash
python -m scripts.calculate_trends
```

### Reset NLP-generated data

```bash
python -m scripts.reset_nlp_data
```

## Launch the Dashboard

```bash
streamlit run ui/app.py
```

## Documentation

The repository includes operational documentation in:

- [docs/api.md](docs/api.md)
- [docs/architecture.md](docs/architecture.md)
- [docs/runbook.md](docs/runbook.md)

## Notes

- The system uses SQLite for local persistence.
- The UI is built with Streamlit and is intended for operational monitoring and trend inspection.
- The data pipeline is separated into ingestion, NLP, and trend scoring stages for easier debugging and reprocessing.

## License

This project is currently maintained as a local development repository. Add a formal license file if you plan to publish it publicly for broader reuse.
