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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
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
    path('book/<int:pk>/<int:page>/', views.bookpage, name="bookpage"),
    path('book/<int:pk>/', views.bookredir, name="bookredir"),
    path('chapter/<int:book>/<int:number>/<int:page>/', views.chapterpage, name="chapterpage"),
    path('chapter/<int:book>/<int:number>/',views.chapterentry,name="chapterpagepageNX"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path("logout/",auth_views.LogoutView.as_view(next_page="/"), name="log out"),
    path('signup/', views.signup, name="sign up"),
    path('bookmarkpress/',views.bookmark, name="bookmark press"),
    path('chaptereditor/<int:book>/<str:chapter>/',views.chaptereditor, name="chapter editor"),
    path('bookeditor/<int:book>/', views.bookEditor, name="book editor"),
    path('submitbook/<int:book>/',views.submitbook, name="book poster"),
    path('deletebook/<int:book>/',views.deletebook, name="book deleter"),
    path('submitchapter/<int:chapterid>/', views.submitchapter, name="chapter poster"),
    path('deletechapter/<int:chapterid>/', views.deletechapter, name="chapter deleter"),
    path('comment/',views.postcomment,name="commentpost"),
    path('deletecomment/<int:pk>/', views.deletecomment,name="deletecomment"),
    path('review/',views.createReview, name="reviewpost"),
    path('deletereview/<int:pk>/', views.deletereview,name="deletereview"),
    path('search/<int:page>/', views.search, name='search'),

    #REST STUFF
    path('api/exists/',views.userExists,name="checkexists"),
    url('api/auth/', include('rest_auth.urls')),
    url('api/auth/registration/', include('rest_auth.registration.urls')),
    path('api/hot/<int:page>/', views.apiPopularBooks, name="api hot"),
    path('api/new/<int:page>/', views.apiNewBooks, name="api new"),
    path('api/top/<int:page>/', views.apiTopRated, name="api top"),
    path('api/whoami/', views.whoami,name="interrogate-self"), #added this in because DRAuth does not provide whether you are staff
    path('api/profile/', views.apiProfile, name="api profile"),
    path('api/book/<int:pk>/', views.apiBookpage, name="api book page"),
    path('api/reviews/<int:book>/<int:page>/', views.apiReviews, name="api reviews"),
    path('api/chapter/<int:book>/<int:number>/', views.apiChapterpage, name="api chapter page"),
    path('api/comments/<int:chapter>/<int:page>/', views.apiComments, name="api comments"),
    path('api/bookmark/<int:book>/', views.apiBookmark, name="api bookmark press"),
    path('api/editBook/', views.apiBookEditor, name="api book editor"),
    path('api/bookPost/', views.apiSubmitbook, name="api book poster"),
    path('api/deleteBook/<int:book>/', views.apiDeletebook, name="api book deleter"),
    path('api/chapterPost/', views.apiSubmitchapter, name="api chapter poster"),
    path('api/chapterEdit/', views.apiChapterEdit, name="api chapter editor"),
    path('api/chapterDelete/<int:chapterid>/', views.apiDeletechapter, name="api chapter deleter"),
    path('api/comment/', views.apiPostcomment, name="api comment post"),
    path('api/commentDelete/<int:pk>/', views.apiDeletecomment, name="api delete comment"),
    path('api/review/', views.apiCreateReview, name="api review post"),
    path('api/reviewDelete/<int:id>/', views.apiDeletereview, name="api delete review"),
    path('api/search/<str:query>/<int:page>/', views.apiSearch, name='search'),
    
]
