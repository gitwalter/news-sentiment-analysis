# This module will handle sentiment analysis using NLP libraries
from textblob import TextBlob
import pandas as pd

def analyze_sentiment(news_df, text_col='description'):
    """
    Adds sentiment polarity and subjectivity columns to the DataFrame using TextBlob.
    """
    def get_sentiment(text):
        if not isinstance(text, str) or not text.strip():
            return 0.0, 0.0
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity

    sentiments = news_df[text_col].fillna('').apply(get_sentiment)
    news_df['polarity'] = [s[0] for s in sentiments]
    news_df['subjectivity'] = [s[1] for s in sentiments]
    # Add sentiment label
    def label(p):
        if p > 0.1:
            return 'positive'
        elif p < -0.1:
            return 'negative'
        else:
            return 'neutral'
    news_df['sentiment'] = news_df['polarity'].apply(label)
    return news_df
