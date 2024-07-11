import requests
import os

class NewsArticleRepository:
    def getNewsArticles(params):
        try:
            params['apiKey'] = os.environ['NEWS_API_KEY']
            r = requests.get('https://newsapi.org/v2/top-headlines', params=params)
            if r.status_code == 200:
                return r.json()['articles']
            return None
        except Exception:
            return None
