
# About This Project

This app was created as a demonstration of the capabilities of AI-assisted software development using GitHub Copilot. The entire development process was a collaboration between a human developer and Copilot, with Copilot providing code, architectural suggestions, and workflow automation at every step.

## How We Built the App Together: Phases in Detail

### Phase 1: Requirements Analysis & Planning
- We began by clarifying the main goal: a Streamlit app for news sentiment analysis, supporting both NewsAPI and RSS feeds.
- Requirements were refined through discussion, with Copilot helping to break down features (news fetching, sentiment analysis, visualization, filtering, export).
- Copilot suggested a modular architecture, separating fetching, sentiment, and visualization logic for maintainability.

### Phase 2: Project Initialization & Structure
- Copilot generated the initial folder structure and boilerplate files, including `main.py` and the `app/` submodules.
- We discussed naming conventions and data flow, with Copilot recommending pandas DataFrames as the standard interface between modules.
- Initial configuration files (requirements.txt, .gitignore) were created with Copilot's input.

### Phase 3: Core Module Implementation
- The news fetching module was built to support both NewsAPI (with API key management) and RSS feeds, using requests and feedparser.
- Sentiment analysis was implemented using TextBlob, with Copilot enforcing polarity thresholds and DataFrame column conventions.
- Visualization tools (word clouds, pie charts) were developed using matplotlib, wordcloud, and plotly, with Copilot providing reusable plotting functions.

### Phase 4: UI Integration & Feature Expansion
- The Streamlit UI was designed iteratively, with Copilot suggesting sidebar patterns, parameter handling, and result display techniques.
- We added features such as language/country/category filters, clickable links, and sentiment icons, with Copilot generating code and handling edge cases.
- Copilot helped debug issues with Streamlit rendering, DataFrame display, and plotly chart integration.

### Phase 5: Testing, Debugging & Validation
- Copilot generated test cases for both NewsAPI and RSS fetching, ensuring coverage of key data flows and error conditions.
- We encountered issues with missing API keys, quota limits, and inconsistent data from different sources; Copilot suggested robust error handling and validation steps.
- Data consistency was enforced by Copilot through interface design and validation, ensuring all modules exchanged data as DataFrames with expected columns.

### Phase 6: Configuration & Library Issues
- During development, we faced several configuration challenges:
   - Version conflicts between matplotlib, wordcloud, and pillow were resolved by Copilot updating requirements and suggesting compatible versions.
   - Streamlit secrets management was set up for secure API key handling, guided by Copilot.
   - Copilot recommended best practices for .gitignore, excluding virtual environments, cache, and config files.
- Copilot also provided troubleshooting steps for common library import errors and environment setup issues.

### Phase 7: Documentation & Project Hygiene
- Copilot assisted in writing a comprehensive README, Copilot instructions, and concept paper, documenting workflows, conventions, and the collaborative process.
- The repository was kept clean and organized with Copilot's guidance on file exclusions and structure.

## Problems and Solutions

- **API Integration:** We encountered issues with NewsAPI authentication and quota. Copilot guided the setup of secrets management and error handling for missing or invalid API keys.
- **Data Consistency:** Ensuring all modules exchanged data as DataFrames required careful interface design. Copilot enforced this convention and added validation steps.
- **Visualization:** Copilot provided reusable functions for word clouds and sentiment charts, and helped debug issues with Streamlit rendering and plotly integration.
- **Testing:** Copilot generated test cases for both NewsAPI and RSS fetching, and suggested ways to mock or skip tests when API keys were missing.
- **Configuration & Library Issues:** Copilot resolved version conflicts, import errors, and environment setup problems by updating requirements and providing troubleshooting steps.
- **.gitignore and Project Hygiene:** Copilot recommended best practices for excluding unnecessary files and keeping the repository clean.

This project demonstrates how Copilot can accelerate development, enforce good practices, and help solve both technical and workflow challenges in real time.
# News Sentiment Analysis

A Streamlit web app for analyzing the sentiment of news articles on any topic. Fetches news from NewsAPI or RSS feeds, applies sentiment analysis, and visualizes results with charts and word clouds.

## Features
- Search news by topic, category, language, country, and more
- Fetch from NewsAPI (API key required) or any RSS feed
- Sentiment analysis using TextBlob (positive, neutral, negative)
- Interactive charts and word clouds for quick insights
- Example headlines grouped by sentiment

## Quickstart
1. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
2. **Set up NewsAPI key (optional, for NewsAPI support):**
   - Add your key to `.streamlit/secrets.toml` as:
     ```toml
     NEWS_API_KEY = "your_api_key_here"
     ```
3. **Run the app:**
   ```powershell
   streamlit run main.py
   ```

## Usage
- Enter a topic and adjust filters in the sidebar
- Click "Fetch News" to analyze
- View sentiment summary, pie chart, word cloud, and sample headlines

## Project Structure
- `main.py` — Streamlit UI and orchestration
- `app/news_fetcher/` — News fetching logic (`fetch_news`)
- `app/sentiment/` — Sentiment analysis (`analyze_sentiment`)
- `app/visualization/` — Visualization tools (`show_wordcloud`)
- `tests/` — Basic tests for news fetching

## Testing
Run all tests with:
```powershell
pytest tests/
```

## Dependencies
See `requirements.txt` for all required packages (notably: `streamlit`, `pandas`, `requests`, `plotly`, `wordcloud`, `matplotlib`, `textblob`).

## Example Code
Fetch and analyze news from NewsAPI:
```python
from app.news_fetcher import fetch_news
from app.sentiment import analyze_sentiment

df = fetch_news('newsapi', query='AI', max_articles=10)
df = analyze_sentiment(df)
```

