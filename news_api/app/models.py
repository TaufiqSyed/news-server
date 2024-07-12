from django.db import models

from news_api.app.utils import null_coalesce

class NewsArticle(models.Model):
    # author = models.CharField(max_length=200, blank=True, null=True)
    # title = models.CharField(max_length=200, blank=True, null=True)
    # description = models.CharField(max_length=200, blank=True, null=True)
    # url = models.CharField(max_length=400, primary_key=True)
    # urlToImage = models.CharField(max_length=400, blank=True, null=True)
    # content = models.CharField(max_length=400, blank=True, null=True)
    # publishedAt = models.DateTimeField(null=True)
    author = models.CharField(max_length=1000, blank=True, null=False)
    title = models.CharField(max_length=1000, blank=True, null=False)
    description = models.CharField(max_length=1000, blank=True, null=False)
    url = models.CharField(max_length=10000, primary_key=True, null=False)
    urlToImage = models.CharField(max_length=1000, blank=True, null=False)
    content = models.CharField(max_length=1000, blank=True, null=False)
    publishedAt = models.DateTimeField(blank=True, null=True)


    class Meta:
        app_label  = 'news_api'
    
    def __str__(self):  
        return f'{self.title} By {self.author}'  
    
    def as_json(self):
        return dict(
            url=self.url,
            author=self.author,
            title=self.title,
            description=self.description,
            urlToImage=self.urlToImage,
            content=self.content,
            publishedAt=null_coalesce(self.publishedAt, self.publishedAt.isoformat()),
        )