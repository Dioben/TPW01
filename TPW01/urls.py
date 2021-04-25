"""TPW01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from app import views
from app.forms import CustomAuthenticationForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('hot/<int:page>/', views.popularBooks, name="hot"),
    path('new/<int:page>/', views.newBooks, name="new"),
    path('top/<int:page>/', views.topRated, name="top"),
    path('profile/', views.userpage, name="profile"),
    path('book/<int:pk>/', views.bookpage, name="bookpage"),
    path('chapter/<int:book>/<int:number>/<int:page>/', views.chapterpage, name="chapterpage"),
    path('chapter/<int:book>/<int:number>/',views.chapterentry,name="chapterpagepageNX"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path("logout/",auth_views.LogoutView.as_view(next_page="/"), name="log out"),
    path('signup/', views.signup, name="sign up"),
    path('bookmarkpress/',views.bookmark, name="bookmark press"),
    path('chaptereditor/<int:book>/<str:chapter>',views.chaptereditor, name="chapter editor"),
    path('bookeditor/<int:book>', views.bookEditor, name="book editor"),
    path('submitbook/<int:book>',views.submitbook, name="book poster"),
    path('deletebook/<int:book>',views.deletebook, name="book deleter"),
    path('submitchapter/<int:chapter>', views.submitchapter, name="chapter poster"),
    path('deletechapter/<int:chapterid>', views.deletechapter, name="chapter deleter"),
    path('comment/',views.postcomment,name="commentpost")
]
