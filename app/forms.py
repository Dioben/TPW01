from django.forms import ModelForm, HiddenInput, TextInput, Textarea, CharField, PasswordInput
from django import forms
from app.models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _

class ReviewForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['text'].strip = False

    novel = forms.IntegerField(widget=HiddenInput)

    class Meta:

        model = Review
        fields = ['rating', 'text',]


class ChapterPostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChapterPostForm, self).__init__(*args, **kwargs)
        self.fields['text'].strip = False

    novel = forms.IntegerField(widget=HiddenInput)
    class Meta:
        model = Chapter
        fields = ['title', 'text']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'text': Textarea(attrs={'class': 'form-control'}),
        }


class BookCreationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookCreationForm, self).__init__(*args, **kwargs)
        self.fields['description'].strip = False

    class Meta:
        model = Book
        fields = ['title', 'description']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'})
        }

class CommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].strip = False

    class Meta:
        model = Comment
        fields = ['chapter','content']
        widgets = {'chapter':HiddenInput(), 'content':Textarea(attrs={'class': 'form-control','rows':"3"})}


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

    username = UsernameField(
        widget=TextInput(
            attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Username'
            }
        )
    )
    password = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(
            attrs={
                'autocomplete': 'current-password',
                'class': 'form-control',
                'placeholder': 'Password'
            }
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    password1 = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control',
                'placeholder': 'Password'
            }
        ),
        help_text="\n".join(password_validation.password_validators_help_texts()),
    )
    password2 = CharField(
        label=_("Password confirmation"),
        widget=PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'form-control',
                'placeholder': 'Password confirmation'
            }
        ),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
        widgets = {'username': TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }
        )}
