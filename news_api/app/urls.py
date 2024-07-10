from .views import NewsArticleView  
from django.urls import path  
  
urlpatterns = [  
    path('news/', NewsArticleView.as_view())  
]  