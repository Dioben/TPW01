from django.forms import ModelForm, HiddenInput, TextInput, Textarea
from app.models import *


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text', 'novel']
        widgets = {'novel': HiddenInput()}


class ChapterPostForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'text', 'novel']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'class': 'form-control'}),
            'novel': HiddenInput()
        }


class BookCreationForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'})
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['chapter','content']
        widgets = {'chapter':HiddenInput(), 'content':Textarea(attrs={'class': 'form-control','rows':"3"})}