from rest_framework import serializers  
from .models import NewsArticle
  
class NewsArticleSerializer(serializers.ModelSerializer):  
    url = serializers.CharField(max_length=10000)
    author = serializers.CharField(max_length=1000, allow_blank=True)
    title = serializers.CharField(max_length=1000, allow_blank=True)
    description = serializers.CharField(max_length=1000, allow_blank=True)
    urlToImage = serializers.CharField(max_length=1000, allow_blank=True)
    content = serializers.CharField(max_length=1000, allow_blank=True)
    publishedAt = serializers.DateTimeField(required=False, allow_null=True)
    
    class Meta:
        model = NewsArticle
        fields = ('__all__')
    # class Meta:  
    #     model = NewsArticle  
    #     fields = ('__all__')  

    def create(self, validated_data):  
        """ 
        Create and return a new `NewsArticle` instance, given the validated data. 
        """  
        return NewsArticle.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
        """ 
        Update and return an existing `NewsArticle` instance, given the validated data. 
        """ 
        instance.author = validated_data.get('author', instance.author)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.url = validated_data.get('url', instance.url)
        instance.urlToImage = validated_data.get('urlToImage', instance.urlToImage)
        instance.content = validated_data.get('content', instance.content)
        instance.publishedAt = validated_data.get('publishedAt', instance.publishedAt)

        instance.save()  
        return instance  