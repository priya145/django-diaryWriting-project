from .models import Book,Dailyfeed
from rest_framework import serializers




class BookSerializers(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'author','published_date','description','price','img']
        

class FeedSerializers(serializers.ModelSerializer):
    class Meta:
        model = Dailyfeed
        fields =['blog_creator','title','slug','blog','created_at']
        