# Copilot Instructions for news-sentiment-analysis

## Project Overview
This project is a Streamlit-based web app for news sentiment analysis. It fetches news articles (via NewsAPI or RSS), analyzes sentiment using TextBlob, and visualizes results (charts, word clouds) for user-specified topics.

## Architecture & Key Components
- `main.py`: Streamlit UI, orchestrates news fetching, sentiment analysis, and visualization.
- `app/news_fetcher/`: Contains `fetch_news()` for retrieving news from NewsAPI (requires `NEWS_API_KEY` in `.streamlit/secrets.toml`) or RSS feeds. Returns a DataFrame with columns: `title`, `description`, `publishedAt`, `url`, `source`.
- `app/sentiment/`: Contains `analyze_sentiment()` which adds `polarity`, `subjectivity`, and `sentiment` (positive/neutral/negative) columns to news DataFrames using TextBlob.
- `app/visualization/`: Contains `show_wordcloud()` for generating word clouds from news titles/descriptions using `wordcloud` and `matplotlib`.
- `tests/`: Contains basic tests for `fetch_news()` (both RSS and NewsAPI).

## Developer Workflows
- **Run the app:**
  ```powershell
  streamlit run main.py
  ```
- **Run tests:**
  ```powershell
  pytest tests/
  ```
- **API Key:**
  - Place your NewsAPI key in `.streamlit/secrets.toml` as `NEWS_API_KEY` for NewsAPI functionality.

## Patterns & Conventions
- All data flows as pandas DataFrames between modules.
- Sentiment is labeled as `positive` (>0.1), `negative` (<-0.1), or `neutral` (otherwise) based on TextBlob polarity.
- UI parameters (topic, filters) are handled in Streamlit sidebar; results and visualizations in main area.
- Word clouds are generated from both `title` and `description` fields.
- NewsAPI and RSS fetching are unified under `fetch_news()`; pass `'newsapi'` or an RSS URL as the `source` argument.

## External Dependencies
- See `requirements.txt` for all dependencies (notably: `streamlit`, `pandas`, `requests`, `plotly`, `wordcloud`, `matplotlib`, `textblob`).
- NewsAPI usage requires a valid API key.

## Examples
- To fetch news from NewsAPI: `fetch_news('newsapi', query='AI', max_articles=10)`
- To fetch from RSS: `fetch_news('http://feeds.bbci.co.uk/news/rss.xml', max_articles=5)`
- To analyze sentiment: `analyze_sentiment(news_df)`
- To show wordcloud: `show_wordcloud(news_df)`

## Testing
- Tests in `tests/test_basic.py` cover both RSS and NewsAPI fetching. NewsAPI tests require a valid API key in secrets.

---
If you add new modules, follow the pattern of returning/accepting DataFrames and keeping UI logic in `main.py`. For questions, see `main.py` and module docstrings for usage patterns.
