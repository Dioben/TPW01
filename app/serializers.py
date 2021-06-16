from rest_framework import serializers
from app.models import *


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id','title','description','reviewcount','scoretotal','chapters','author')


class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Review
        fields = '__all__'


class SimpleChapterSerializer(serializers.Serializer):
    title = serializers.CharField()
    release = serializers.DateTimeField()
    number = serializers.IntegerField()

class ChapterSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="novel.title",read_only=True)
    class Meta:
        model = Chapter
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

