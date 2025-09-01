# fetcher_functions.py
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List, Dict

def fetch_news_articles(api_key: str, company_name: str, days_ago: int = 7) -> List[Dict]:
    """Fetches articles for a company from the last few days using NewsAPI."""
    print(f"Fetching news for '{company_name}'...")
    base_url = "https://newsapi.org/v2/everything"
    from_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    query = f'"{company_name}"'

    params = {
        'q': query,
        'from': from_date,
        'sortBy': 'relevancy',
        'language': 'en',
        'apiKey': api_key,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article_data in data.get('articles', []):
            if article_data.get('content'):
                articles.append({
                    'source': article_data['source']['name'],
                    'title': article_data['title'],
                    'url': article_data['url'],
                    'content': article_data['content'],
                    'published_at': article_data['publishedAt'],
                    'company': company_name
                })
        print(f"Found {len(articles)} articles.")
        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []
    
load_dotenv()
NEWS_API_KEY = "dca2abaa24f349e8ab27170b8b5ebc5f"
articles = fetch_news_articles(NEWS_API_KEY, 'Google')


print("\n--- Fetched Articles ---")
for i, article in enumerate(articles, 1):
    print(f"Article {i}: {article['title']}")
    print(f"URL: {article['url']}")
    print("-" * 20)

