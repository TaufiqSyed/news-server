from django.utils.dateparse import parse_datetime
from django.shortcuts import render
from news_api.app.repositories import NewsArticleRepository
from news_api.app.utils import null_coalesce
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .models import NewsArticle  
from .serializers import NewsArticleSerializer
from django.http import JsonResponse
import requests
import json 
from datetime import datetime
class NewsArticleView(APIView):
    def __init__(self):
        super()
        self.countries = ["ae","ar","at","au","be","bg","br","ca","ch","cn","co","cu","cz","de","eg","fr","gb","gr","hk","hu","id","ie","il","in","it","jp","kr","lt","lv","ma","mx","my","ng","nl","no","nz","ph","pl","pt","ro","rs","ru","sa","se","sg","si","sk","th","tr","tw","ua","us","ve","za"]
        self.categories = ['business','entertainment','general','health','science','sports','technology']
        self.optional_params = ['q', 'country', 'category', 'sources']
        self.mandatory_params = ['pageSize', 'page']

    def get(self, request, *args, **kwargs):  
        params = request.query_params.copy()
        err_resp = self.validate_param_fields(params)
        if err_resp is not None: return err_resp

        repo = NewsArticleRepository(params)
        try:
            news_articles = repo.getNewsArticles()
            articles = news_articles
            return JsonResponse({'status': 'success', 'articles': list(map(lambda x: x.as_json(), articles))}, status=200)  
        except Exception as e:
            print(e)
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
        too_vague = not any(x in params for x in self.optional_params)
        if too_vague:
            return Response(
                    {
                        'status': 'failure',
                        'error': f'Search is too vague - must have at least one condition'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        incompatible_filters = 'sources' in params and ('category' in params or 'country' in params)
        if incompatible_filters:
            return Response(
                    {
                        'status': 'failure',
                        'error': f'Filtering by sources cannot mix with country / category filters'
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        for param in params:
            validator = getattr(self, f"validate_{param}")
            if not validator(params[param]):
                return Response({'status': 'failure', 'error': f'Invalid parameter `{param}: {params[param]}`'}, status=400) 

    
    def validate_q(self, s):
        return len(s) <= 500
    
    def validate_country(self, s):
        return s in self.countries

    def validate_category(self, s):
        return s in self.categories

    def validate_sources(self, s):
        r = requests.get('https://newsapi.org/v2/top-headlines/sources?apiKey=a022f5e533e245f2ae741a6ff9c27cf9')
        if r.status_code == 200:
            result = r.json()['sources']
            valid_ids = {x['id'] for x in result}
            for src in s.split(','):
                if src not in valid_ids: return False
            return True
        return False

    def validate_pageSize(self, s):
        try:
            val = int(s)
            if val < 0: return False
            return True
        except ValueError:
            return False
        
    def validate_page(self, s):
        try:
            val = int(s)
            if val < 0: return False
            return True
        except ValueError:
            return False
