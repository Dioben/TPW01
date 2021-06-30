from django.db import models
from django.contrib.auth.models import User
from django.core.validators import *
# Create your models here.
from django.db.models import CASCADE,DO_NOTHING


class Book(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=5000)
    author = models.ForeignKey(User, on_delete=CASCADE)
    reviewcount = models.IntegerField(default=0)  # always compute score via these I guess
    scoretotal = models.BigIntegerField(default=0)
    chapters = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    bookmarks = models.ManyToManyField(User, related_name="bookmarks", blank=True)
    cover = models.CharField(max_length=200,default="https://i.imgur.com/EWudfXq.png")

class Review(models.Model):
    class Meta:
        unique_together = (('author', 'novel'),)

    author = models.ForeignKey(User, on_delete=DO_NOTHING)
    novel = models.ForeignKey(Book, on_delete=CASCADE)
    rating = models.IntegerField(default=100, validators=[MinValueValidator(0), MaxValueValidator(100)])
    release = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=5000)


class Chapter(models.Model):
    title = models.CharField(max_length=150)
    text = models.CharField(max_length=50000)  # TODO: CONSIDER IMPORTING RICH TEXT FIELDS
    novel = models.ForeignKey(Book, on_delete=CASCADE)
    release = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField(validators=[MinValueValidator(1)])


class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=DO_NOTHING)
    chapter = models.ForeignKey(Chapter, on_delete=CASCADE)
    content = models.CharField(max_length=1000)
    release = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=CASCADE)


class LastRead(models.Model):
    class Meta:
        unique_together = (('author', 'book'),)
    author = models.ForeignKey(User, on_delete=CASCADE)
    book = models.ForeignKey(Book, on_delete=CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=CASCADE)

