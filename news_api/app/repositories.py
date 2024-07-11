import requests
import os

from django.core import serializers
from news_api.app.models import NewsArticle

class NewsArticleRepository:
    def getNewsArticles(params):
        # NewsArticle.objects.all().delete()

        # queryset = NewsArticle.objects.all()
        # json_data = serializers.serialize('json', queryset)
        # print(json_data)

        try:
            params['apiKey'] = os.environ['NEWS_API_KEY']
            r = requests.get('https://newsapi.org/v2/top-headlines', params=params)
            if r.status_code == 200:
                return r.json()['articles']
            return None
        except Exception:
            return None
