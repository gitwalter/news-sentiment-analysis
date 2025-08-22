

import streamlit as st
import pandas as pd
from app.news_fetcher import fetch_news
from app.visualization import show_wordcloud

st.set_page_config(page_title="News Sentiment Analysis", layout="wide")
st.title("News Sentiment Analysis")



topic = st.text_input("Enter a topic to search for news:", value="artificial intelligence")

# Move all search/filter parameters except topic to sidebar
with st.sidebar:
	st.header("Search Filters")
	# NewsAPI supported categories
	categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
	category = st.selectbox("Select news category (optional):", ["All"] + categories)

	# NewsAPI supported languages
	languages = [
		("ar", "Arabic"), ("de", "German"), ("en", "English"), ("es", "Spanish"), ("fr", "French"),
		("he", "Hebrew"), ("it", "Italian"), ("nl", "Dutch"), ("no", "Norwegian"), ("pt", "Portuguese"),
		("ru", "Russian"), ("se", "Northern Sami"), ("ud", "Urdu"), ("zh", "Chinese")
	]
	lang_options = [f"{code} - {name}" for code, name in languages]
	selected_langs = st.multiselect("Select language(s):", lang_options, default=["en - English"])
	selected_lang_codes = [l.split(" - ")[0] for l in selected_langs]

	# NewsAPI supported countries
	countries = ["ae","ar","at","au","be","bg","br","ca","ch","cn","co","cu","cz","de","eg","fr","gb","gr","hk","hu","id","ie","il","in","it","jp","kr","lt","lv","ma","mx","my","ng","nl","no","nz","ph","pl","pt","ro","rs","ru","sa","se","sg","si","sk","th","tr","tw","ua","us","ve","za"]
	country = st.selectbox("Select country (for top-headlines):", ["All"] + countries)

	sources = st.text_input("News sources (comma-separated, e.g. bbc-news,the-verge):", value="")
	domains = st.text_input("Domains (comma-separated, e.g. bbc.co.uk,techcrunch.com):", value="")
	from_date = st.date_input("From date", value=None, key="from_date")
	to_date = st.date_input("To date", value=None, key="to_date")
	sort_by = st.selectbox("Sort by:", ["publishedAt", "relevancy", "popularity"])
	page = st.number_input("Page number", min_value=1, value=1)
	num_news = st.number_input("Number of news to fetch:", min_value=1, max_value=100, value=20)

fetch_btn = st.button("Fetch News")

if fetch_btn and topic:
	with st.spinner(f"Fetching news for '{topic}'..."):
		cat = None if category == "All" else category
		country_val = None if country == "All" else country
		# Fetch news for all selected languages and concatenate
		news_dfs = []
		for lang in selected_lang_codes:
			news = fetch_news(
				'newsapi',
				query=topic,
				max_articles=num_news,
				category=cat,
				sources=sources if sources else None,
				domains=domains if domains else None,
				date_range=(str(from_date) if from_date else None, str(to_date) if to_date else None),
				language=lang,
				sort_by=sort_by,
				page=page,
				country=country_val
			)
			news_dfs.append(news)
		news_df = pd.concat(news_dfs, ignore_index=True) if news_dfs else pd.DataFrame()
	if not news_df.empty:
		st.subheader(f"Top News for '{topic}'")
		from app.sentiment import analyze_sentiment
		news_df = analyze_sentiment(news_df)
		# Show sentiment label counts
		sentiment_counts = news_df['sentiment'].value_counts().reindex(['positive', 'neutral', 'negative'], fill_value=0)
		col_summary, col_chart = st.columns([2, 1])
		with col_summary:
			st.markdown("### Sentiment Summary")
			st.write(sentiment_counts)
		with col_chart:
			st.markdown("### ")  # Empty header for alignment
			import plotly.express as px
			pie_df = sentiment_counts.reset_index()
			pie_df.columns = ['Sentiment', 'Count']
			fig = px.pie(
				pie_df,
				names='Sentiment',
				values='Count',
				color='Sentiment',
				color_discrete_map={'positive': '#4CAF50', 'neutral': '#FFEB3B', 'negative': '#F44336'},
				hole=0.3
			)
			fig.update_traces(textinfo='percent+label', textfont_size=12)
			st.plotly_chart(fig, use_container_width=False)

	# Helper functions for table display
	def color_sentiment_row(row):
		color = {
			'positive': 'background-color: #d4edda; color: #155724;',
			'neutral': 'background-color: #ffe066; color: #333;',
			'negative': 'background-color: #f8d7da; color: #721c24;'
		}
		return [color.get(row['sentiment'], '')]*len(row)

	def sentiment_icon(val):
		icons = {'positive': '🟢', 'neutral': '🟡', 'negative': '🔴'}
		return icons.get(val, '')

	def make_clickable(val):
		return f'<a href="{val}" target="_blank">link</a>' if pd.notnull(val) and val else ''

	if not news_df.empty:
		# Ensure all expected columns exist
		for col in ['title', 'source', 'url', 'sentiment']:
			if col not in news_df.columns:
				news_df[col] = ''
		display_df = news_df[['title', 'source', 'url', 'sentiment']].copy()
		display_df['sentiment_icon'] = display_df['sentiment'].apply(sentiment_icon)
		display_df['link'] = display_df['url'].apply(make_clickable)
		# Scrollable news table
		styled = display_df[['title', 'source', 'link', 'sentiment_icon', 'sentiment']].style.apply(color_sentiment_row, axis=1)
		styled = styled.hide(axis='columns', subset=['sentiment'])
		styled = styled.set_properties(subset=['sentiment_icon'], **{'text-align': 'center'})
		st.markdown(
			f'<div style="max-height: 500px; overflow-y: auto;">{styled.to_html(escape=False, index=False)}</div>',
			unsafe_allow_html=True
		)

		# Show sample headlines for each sentiment
		st.markdown("### Example Headlines by Sentiment")
		for label, color in zip(['positive', 'neutral', 'negative'], ['🟢', '🟡', '🔴']):
			subset = news_df[news_df['sentiment'] == label]
			if not subset.empty:
				st.markdown(f"**{color} {label.capitalize()} News:**")
				for t in subset['title'].head(3):
					st.markdown(f"- {t}")

		st.subheader("Word Cloud of News Titles and Descriptions")
		show_wordcloud(news_df)
	else:
		st.warning("No news found. Check your API key or try another topic.")
