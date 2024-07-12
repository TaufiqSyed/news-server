from django.db import models
from news_api.app.utils import null_coalesce
import architect

@architect.install('partition', type='range', subtype='date', constraint='month', column='publishedAt')
class NewsArticle(models.Model):
    url = models.CharField(max_length=10000, null=False, blank=False, unique=True, primary_key=True)
    author = models.CharField(max_length=1000, blank=True, null=False, primary_key=False)
    title = models.CharField(max_length=1000, blank=True, null=False)
    description = models.CharField(max_length=1000, blank=True, null=False)
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

    