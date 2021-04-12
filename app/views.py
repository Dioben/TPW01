from django.shortcuts import render
from models import *
# Create your views here.

#HOME PAGE
#TODO: put something in index.html/index.js
# make a login/sign in page AFTER we learn how that stuff works
# load latest chapters and top rated fics onto frontpage
# user profile page allowing new-book creation, also viewing and changing all reviews in another tab maybe?
# i dont want user stats but that's just cuz they're a pain, we can add them in
# book page allowing anyone to select chapters, allowing normal users to review and allowing the author to move into the chapter creation menu
# REST for making/deleting/editing (description and title only) a book
# REST for adding/removing/editing chapters
# CHAPTER READING PAGE INCLUDING COMMENTS, CONSIDER USING PAGING FOR COMMENTS JUST 'CAUSE (no clue how to make hierarchical comments work in django templating btw)
#  REST STUFF SHOULD BE IN DIFFERENT FILES, MAKE FILES FOR GET,POST AND DELETE POSSIBLY
# also we should consider JS submitting over <form>, i just sort of don't like forms on viewside
def index(request):
    data = {}
    return render(request, "index.html", data)


def latest(request):
    return Chapter.objects.reverse()[:20] #hopefully the last 20 chapters with books attached


def popular(request):
    return Book.objects.order_by("scoretotal/reviewcount") #unsure whether this works, just needs to be the books



