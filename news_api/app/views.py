from django.shortcuts import render
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from .models import NewsArticle  
from .serializers import NewsArticleSerializer  

class NewsArticleView(APIView):  
    def get(self, request, *args, **kwargs):  
        result = NewsArticle.objects.all()  
        serializers = NewsArticleSerializer(result, many=True)  
        return Response({'status': 'success', "newsarticles":serializers.data}, status=200)  
  
    def post(self, request):  
        serializer = NewsArticleSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)