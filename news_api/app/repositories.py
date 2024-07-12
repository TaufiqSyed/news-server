from datetime import datetime
import json
from sqlite3 import IntegrityError
from django.db.models import Q

import requests
import os

from django.core import serializers
from news_api.app.models import NewsArticle
from news_api.app.serializers import NewsArticleSerializer
from news_api.app.utils import null_coalesce

class NewsArticleRepository:
    def __init__(self, params):
        self.params = params
        self.params['apiKey'] = os.environ['NEWS_API_KEY']
        self.page = int(self.params['page'])
        self.pageSize = int(self.params['pageSize'])

    def getNewsArticles(self):
        # print(self.params)
        db_articles = self.getNewsArticlesFromDb()
        # print('DB Articles', db_articles)
        print('Number of articles from database =', len(db_articles))
        num_retrieved = len(db_articles)
        num_requested = self.pageSize - num_retrieved
        if num_requested == 0: return db_articles
        article_set = {article.url for article in db_articles}
        api_articles = self.getNewsArticlesFromApi(num_requested, article_set)
        print('Number of articles from API =', len(api_articles))
        # print('API Articles', api_articles)
        
        return db_articles + api_articles

        
    def getNewsArticlesFromDb(self):
        offset = (self.page-1)*self.pageSize
        queryset = NewsArticle.objects.all()

        if 'country' in self.params and self.params['country'] != '' and self.params['country'] is not None:
            queryset = queryset.filter(
                Q(title__contains=self.params['country']) | 
                Q(content__contains=self.params['country']) |
                Q(description__contains=self.params['country'])
            )
        
        if 'category' in self.params and self.params['category'] != '' and self.params['category'] is not None:
            queryset = queryset.filter(
                Q(title__contains=self.params['category']) | 
                Q(content__contains=self.params['category']) |
                Q(description__contains=self.params['category'])
            )

        if 'q' in self.params and self.params['q'] != '' and self.params['q'] is not None:
            queryset = queryset.filter(
                Q(title__contains=self.params['q']) | 
                Q(content__contains=self.params['q']) |
                Q(description__contains=self.params['q'])
            )
        
        queryset = queryset.order_by('-publishedAt')[offset:offset+self.pageSize]
        return list(queryset)


    def getNewsArticlesFromApi(self, num_requested=None, article_set=None):
        article_set = null_coalesce(article_set, set())
        num_requested = null_coalesce(num_requested, self.pageSize)
        margin_of_error = 0 # number of extra articles to fetch in case of duplicate
        num_to_fetch = num_requested + margin_of_error
        factor = self.pageSize // num_to_fetch
        self.params['page'] = ((self.page*self.pageSize)//num_to_fetch)-factor+1
        self.params['pageSize'] = num_to_fetch
        result = []
        try:
            while num_to_fetch > 0: 
                r = requests.get('https://newsapi.org/v2/top-headlines', params=self.params)
                if r.status_code == 200:
                    fetched = r.json()['articles']
                    print(fetched)
                    if len(fetched) == 0:
                        break
                    fetched = list(filter(lambda x: x['url'] not in article_set, fetched))
                    if len(fetched) > num_to_fetch:
                        num_to_fetch = 0
                        result.extend(fetched[:num_to_fetch])
                    else:
                        num_to_fetch -= len(fetched)
                        result.extend(fetched)
                        self.params['page'] += 1
                else:
                    raise ValueError
        except Exception as e:
            result = None
        self.params['page'] = str(self.page)
        self.params['pageSize'] = str(self.pageSize)
        objects = self.cleanApiData(result)
        # print(objects)
        self.add_articles_to_db(objects)
        return objects
        

    def cleanApiData(self, news_articles):
        articles = []
        for article_data in news_articles:
            article_data['publishedAt'] = null_coalesce(article_data['publishedAt'], None)
            article_data['author'] = null_coalesce(article_data['author'], '')
            article_data['title'] = null_coalesce(article_data['title'], '')
            article_data['description'] = null_coalesce(article_data['description'], '')
            article_data['urlToImage'] = null_coalesce(article_data['urlToImage'], '')
            article_data['content'] = null_coalesce(article_data['content'], '')
            serializer = NewsArticleSerializer(data=article_data)
            if serializer.is_valid():
                articles.append(NewsArticle(**serializer.validated_data))
            else:
                print(serializer.errors)
                raise ValueError
        return articles
        # return list(map(lambda x: x.as_json(), articles))

    def add_articles_to_db(self, articles):
        for obj in articles:
            try:
                obj.save()
            except IntegrityError:
                continue
    