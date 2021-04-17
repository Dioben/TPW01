from django.forms import ModelForm,HiddenInput
from app.models import *

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['rating','text','novel']
        widgets = {'novel': HiddenInput()}

class ChapterPostForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ['title','text','novel']
        widgets = {'novel': HiddenInput()}

class BookCreationForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title','description']