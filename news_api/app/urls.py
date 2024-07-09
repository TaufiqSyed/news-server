from .views import NewsArticleView  
from django.urls import path  
  
urlpatterns = [  
    path('basic/', NewsArticleView.as_view())  
]  