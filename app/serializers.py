from rest_framework import serializers
from app.models import *


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username",read_only=True)
    class Meta:
        model = Book
        fields = ('id','title','description','reviewcount','scoretotal','chapters','author','author_name')


class ReviewSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Review
        fields = '__all__'


class SimpleChapterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    release = serializers.DateTimeField()
    number = serializers.IntegerField()

class ChapterSerializer(serializers.ModelSerializer):
    book_name = serializers.CharField(source="novel.title",read_only=True)
    author_name = serializers.CharField(source="novel.author.username",read_only=True)
    total_chapters = serializers.IntegerField(source="novel.chapters",read_only=True)
    book_cover = serializers.CharField(source="novel.cover",read_only=True)
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
        fields = ('username', 'email', 'id')


class PostCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    content = serializers.CharField()
    chapter = serializers.PrimaryKeyRelatedField(queryset=Chapter.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True)
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Comment
        exclude = ['release']


class PostReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    novel = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    rating = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    text = serializers.CharField(max_length=5000)

    class Meta:
        model = Review
        exclude = ['release', 'author']

class PostBookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=150)
    description = serializers.CharField(max_length=5000)
    cover = serializers.CharField(required=False)
    class Meta:
        model = Book
        fields = ('id', 'title', 'description')


class PostChapterSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    title = serializers.CharField(max_length=150)
    text = serializers.CharField(max_length=50000)
    novel = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Chapter
        exclude = ['release', 'number']
