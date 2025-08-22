import requests
import feedparser
import streamlit as st
import pandas as pd
from datetime import datetime

def fetch_news(source, query=None, date_range=None, max_articles=20, category=None, sources=None, domains=None, language=None, sort_by=None, page=None, country=None):
    """
    Fetch news articles from NewsAPI or RSS feed.
    Args:
        source (str): 'newsapi' or RSS feed URL
        query (str): search keyword
        date_range (tuple): (from_date, to_date) in 'YYYY-MM-DD' format
        max_articles (int): max number of articles to fetch
    Returns:
        pd.DataFrame: DataFrame with columns ['title', 'description', 'publishedAt', 'url', 'source']
    """
    articles = []
    if source == 'newsapi':
        api_key = st.secrets.get('NEWS_API_KEY', None)
        if not api_key:
            st.error('NEWS_API_KEY not found in Streamlit secrets.')
            return pd.DataFrame()
        if category or country:
            url = 'https://newsapi.org/v2/top-headlines'
            params = {
                'q': query or '',
                'category': category,
                'sources': sources,
                'country': country,
                'apiKey': api_key,
                'pageSize': max_articles,
                'language': language or 'en',
                'page': page
            }
        else:
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': query or '',
                'from': date_range[0] if date_range else None,
                'to': date_range[1] if date_range else None,
                'sources': sources,
                'domains': domains,
                'sortBy': sort_by or 'publishedAt',
                'apiKey': api_key,
                'pageSize': max_articles,
                'language': language or 'en',
                'page': page
            }
        # Remove None values
        params = {k: v for k, v in params.items() if v not in [None, '', 'All']}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            for a in data.get('articles', []):
                articles.append({
                    'title': a['title'],
                    'description': a['description'],
                    'publishedAt': a['publishedAt'],
                    'url': a['url'],
                    'source': a['source']['name']
                })
        else:
            st.error(f"NewsAPI error: {response.status_code}")
    else:
        # Assume RSS feed URL
        feed = feedparser.parse(source)
        for entry in feed.entries[:max_articles]:
            published = entry.get('published', '')
            try:
                published = datetime(*entry.published_parsed[:6]).isoformat()
            except Exception:
                pass
            articles.append({
                'title': entry.get('title', ''),
                'description': entry.get('summary', ''),
                'publishedAt': published,
                'url': entry.get('link', ''),
                'source': feed.feed.get('title', 'RSS')
            })
    return pd.DataFrame(articles)
