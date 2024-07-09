from django.db import models

class NewsArticle(models.Model):
    author = models.CharField(max_length=200)  
    title = models.CharField(max_length=200)  
    description = models.CharField(max_length=200)  
    url = models.CharField(max_length=400)  
    urlToImage = models.CharField(max_length=400)
    content = models.CharField(max_length=400)
    publishedAt = models.DateTimeField()

    class Meta:
        app_label  = 'news_api'
    
    def __str__(self):  
        return f'{self.title} By {self.last_name}'  