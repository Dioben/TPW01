from django.shortcuts import render

from app.commonqueries import *
from models import *
# Create your views here.

#TODO:
# put something in index.html/index.js
# make a login/sign in page AFTER we learn how that stuff works -> on hold until p class I guess
# load latest chapters and top rated fics onto frontpage -> NEW IDEA: HOT CAN BE WHATEVER HAS GOTTEN MOST RATING IN LAST X HOURS
# user profile page allowing new-book creation
# user profile page viewing and changing all reviews in another tab maybe? - may be too much for this project (leave for last)
# i dont want user stats but that's just cuz they're a pain, we can add them in - not that important (leave for last)
# book page allowing anyone to select chapters, allowing normal users to review and allowing the author to move into the chapter creation menu
# REST for making/deleting/editing (description and title only) a book
# REST for adding/removing/editing chapters
# CHAPTER READING PAGE INCLUDING COMMENTS, CONSIDER USING PAGING FOR COMMENTS JUST 'CAUSE (no clue how to make hierarchical comments work in django templating btw)
# REST STUFF SHOULD BE IN DIFFERENT FILES, MAKE FILES FOR GET,POST AND DELETE POSSIBLY
# also we should consider JS submitting over <form>, i just sort of don't like forms on viewside
# allow any user to save books for easy access in a following page
# maybe save which books and what chapter the user read (history)
# top rated/ hot pages / new pages


# HOME PAGE
def index(request):
    data = { 'newchaps' : Chapter.objects.order_by("-release").select_related()[:10], 'toprated': bookbyrating(total=10), 'rising': bookrisingpop(total=10)}
    return render(request, "index.html", data)


def bookpage(request, pk):
    data = {'book': Book.objects.select_related().get(pk=pk)}
    data['chapters'] = Chapter.objects.only("title", "number", "release").filter(novel=data['book'])
    data['reviews'] = Review.objects.filter(novel=data['book']).select_related('author')
    #if request. TODO: IF USER AUTH'D ALSO QUERY LAST READ AND BOOKMARKED VALUES
    return render(request, 'book.html', data)


def topRated(request,page):
    data = {'sorttype': 'By Rating', 'books': bookbyrating(page)}
    return render(request, 'listing.html', data)


def popularBooks(request,page):
    data = {'sorttype': 'By Rating', 'books': bookrisingpop(page)}
    return render(request, 'listing.html', data)


def newBooks(request,page):
    data = {'sorttype': 'By Rating', 'books': bookbynew(page)}
    return render(request, 'listing.html', data)
