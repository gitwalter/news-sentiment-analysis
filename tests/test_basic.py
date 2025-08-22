import pandas as pd
import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app.news_fetcher import fetch_news

def test_fetch_news_rss():
    # Example RSS feed (BBC)
    rss_url = 'http://feeds.bbci.co.uk/news/rss.xml'
    df = fetch_news(rss_url, max_articles=3)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert set(['title', 'description', 'publishedAt', 'url', 'source']).issubset(df.columns)

# To test NewsAPI, set NEWS_API_KEY in .streamlit/secrets.toml and uncomment below:

def test_fetch_news_newsapi():
    # Requires NEWS_API_KEY in .streamlit/secrets.toml

    df = fetch_news('newsapi', query='artificial intelligence', max_articles=3)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty, "No news returned from NewsAPI. Check API key and quota."
    assert set(['title', 'description', 'publishedAt', 'url', 'source']).issubset(df.columns)
