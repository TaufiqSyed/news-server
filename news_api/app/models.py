from django.db import models

class NewsArticle(models.Model):
    # author = models.CharField(max_length=200, blank=True, null=True)
    # title = models.CharField(max_length=200, blank=True, null=True)
    # description = models.CharField(max_length=200, blank=True, null=True)
    # url = models.CharField(max_length=400, primary_key=True)
    # urlToImage = models.CharField(max_length=400, blank=True, null=True)
    # content = models.CharField(max_length=400, blank=True, null=True)
    # publishedAt = models.DateTimeField(null=True)
    author = models.CharField(max_length=200, blank=True, null=False)
    title = models.CharField(max_length=200, blank=True, null=False)
    description = models.CharField(max_length=200, blank=True, null=False)
    url = models.CharField(max_length=400, primary_key=True, null=False)
    urlToImage = models.CharField(max_length=400, blank=True, null=False)
    content = models.CharField(max_length=400, blank=True, null=False)
    publishedAt = models.DateTimeField(blank=True, null=True)


    class Meta:
        app_label  = 'news_api'
    
    def __str__(self):  
        return f'{self.title} By {self.last_name}'  