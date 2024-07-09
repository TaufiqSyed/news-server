from django.shortcuts import render
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .models import NewsArticle  
from .serializers import NewsArticleSerializer  
import requests
import json 

class NewsArticleView(APIView):  
    def get(self, request, *args, **kwargs):  
        # result = NewsArticle.objects.all()
        # NewsArticle.objects.all()
        r = requests.get('https://newsapi.org/v2/everything?q=bitcoin&apiKey=a022f5e533e245f2ae741a6ff9c27cf9', params=request.GET)
        if r.status_code == 200:
            result = r.json()['articles']
            return Response({'status': 'success', 'newsarticles': result})
            # print(type(result))
            # print(result[0])
            # print(type(result[0]))
            # res = json.load(result)
            # print(res[0])
            # serializers = NewsArticleSerializer(result, many=True)  
            # return Response({'status': 'success', 'newsarticles': serializers})
        return Response({'status': 'failure'}, status=500)  
  
    def post(self, request):  
        serializer = NewsArticleSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)