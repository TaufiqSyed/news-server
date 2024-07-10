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
        self.optional_params = ['q', 'from', 'to', 'sortBy', 'sources', 'language']
        self.mandatory_params = ['pageSize', 'page']

    def get(self, request, *args, **kwargs):  
        params = request.query_params.copy()
        err_resp = self.validate_param_fields(params)
        if err_resp is not None: return err_resp

        news_articles = NewsArticleRepository.getNewsArticles(params)
        if news_articles is not None:
            return Response({'status': 'success', 'articles': news_articles}, status=200)  
        else:
            return Response({'status': 'failure'}, status=500)  
  
    def validate_param_fields(self, params):
        for param in self.mandatory_params:
            if param not in params:
                return Response(
                    {
                        'status': 'failure',
                        'error': f'Missing required parameter: {param}'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        for param in params:
            if param not in self.mandatory_params and param not in self.optional_params:
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
                return Response({'status': 'failure', 'error': f'Invalid parameter `{param}: {params[param]}`'}, status=400) 

    
    def validate_q(self, s):
        return len(s) <= 500
    
    def validate_from(self, s):
        try:
            datetime.fromisoformat(s)
        except:
            return False
        return True
    
    def validate_to(self, s):
        try:
            datetime.fromisoformat(s)
        except:
            return False
        return True

    def validate_sortBy(self, s):
        return s in ['relevancy', 'popularity', 'publishedAt']
    
    def validate_sources(self, s):
        r = requests.get('https://newsapi.org/v2/top-headlines/sources?apiKey=a022f5e533e245f2ae741a6ff9c27cf9')
        if r.status_code == 200:
            result = r.json()['sources']
            valid_ids = {x['id'] for x in result}
            for src in s.split(','):
                if src not in valid_ids: return False
            return True
        return False

    
    # def post(self, request):  
    #     serializer = NewsArticleSerializer(data=request.data)  
    #     if serializer.is_valid():  
    #         serializer.save()  
    #         return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
    #     else:  
    #         return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)