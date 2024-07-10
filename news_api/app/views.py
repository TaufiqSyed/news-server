from django.shortcuts import render
from news_api.app.repositories import NewsArticleRepository
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .models import NewsArticle  
from .serializers import NewsArticleSerializer  
import requests
import json 
from datetime import datetime
class NewsArticleView(APIView):
    def __init__(self):
        super()
        self.optional_params = ['q', 'from', 'sortBy', 'sources' 'language']

    def get(self, request, *args, **kwargs):  
        params = request.query_params.copy()
        self.validate_param_fields(params)
        news_articles = NewsArticleRepository.getNewsArticles(params)
        if news_articles is not None:
            return Response({'status': 'success', 'articles': news_articles}, status=200)  
        else:
            return Response({'status': 'failure'}, status=500)  
  
    def validate_param_fields(self, params):
        for param in params:
            if param not in self.optional_params:
               return Response(
                    {
                        'status': 'failure',
                        'error': f'Unsupported parameter: {param}'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
        for param in params:
            validator = getattr(self, f"validate_{param}")
            if not validator(params[param]):
                return Response({'status': 'failure', 'error': f'Invalid {param}: "{params['param']}"'}, status=500) 

    
    def validate_q(self, s):
        return len(s) <= 500
    
    def validate_from(self, s):
        try:
            datetime.fromisoformat(s)
        except:
            return False
        return True

    def validate_sortBy(self, s):
        return s in ['relevancy', 'popularity', 'publishedAt']
    
    def validate_sources(self, s):
        r = requests.get('https://newsapi.org/v2/top-headlines/sources?apiKey=a022f5e533e245f2ae741a6ff9c27cf9', params=request.GET)
        if r.status_code == 200:
            result = r.json()['sources']
            valid_ids = {x['id'] for x in result}
            for src in s.split(','):
                if src not in valid_ids: return False
            # return Response({'status': 'success', 'newsarticles': result})
            # print(type(result))
            # print(result[0])
            # print(type(result[0]))
            # res = json.load(result)
            # print(res[0])
            # serializers = NewsArticleSerializer(result, many=True)  
            # return Response({'status': 'success', 'newsarticles': serializers})
        return False
        # return Response({'status': 'failure'}, status=500) 

    
    # def post(self, request):  
    #     serializer = NewsArticleSerializer(data=request.data)  
    #     if serializer.is_valid():  
    #         serializer.save()  
    #         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
    #     else:  
    #         return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)