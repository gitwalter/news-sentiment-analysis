# This module will handle visualizations (charts, word clouds, etc.)
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def show_wordcloud(news_df):
    text = ' '.join(news_df['title'].fillna('')) + ' ' + ' '.join(news_df['description'].fillna(''))
    if not text.strip():
        st.info("No text available for wordcloud.")
        return
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
