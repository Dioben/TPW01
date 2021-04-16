from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from app.commonqueries import *
from app.creationMethods import *
from models import *
# Create your views here.

#TODO:
# put something in index.html/index.js
# user profile page allowing new-book creation
# user profile page viewing and changing all reviews in another tab maybe? - may be too much for this project (leave for last)
# i dont want user stats but that's just cuz they're a pain, we can add them in - not that important (leave for last)
# book page allowing anyone to select chapters, allowing normal users to review and allowing the author to move into the chapter creation menu
# REST for making/deleting/editing (description and title only) a book
# REST for adding/removing/editing chapters
# MOVE TO FORMS

#DONE ON SERVER END
# load latest chapters and top rated fics onto frontpage -> NEW IDEA: HOT CAN BE WHATEVER HAS GOTTEN MOST RATING IN LAST X HOURS
# CHAPTER READING PAGE INCLUDING COMMENTS, CONSIDER USING PAGING FOR COMMENTS JUST 'CAUSE (no clue how to make hierarchical comments work in django templating btw)
# top rated/ hot pages / new pages -> just needs the view I think
# make a login/sign in page AFTER we learn how that stuff works
#allow any user to save books for easy access in a following page -> bookmarked is a thing, just need to get a form or JS call going browser side

#DONE FOR REAL


# HOME PAGE
def index(request):
    data = { 'newchaps' : Chapter.objects.order_by("-release").select_related()[:10], 'toprated': bookbyrating(total=10), 'rising': bookrisingpop(total=10)}
    return render(request, "index.html", data)


def bookpage(request, pk):
    data = {'book': Book.objects.select_related().get(pk=pk), 'lastread': 0}
    data['chapters'] = Chapter.objects.only("title", "number", "release").filter(novel=data['book'])
    data['reviews'] = Review.objects.filter(novel=data['book']).select_related('author')
    if request.user.is_authenticated:
        lastread = LastRead.objects.get(book_id=pk,author=request.user)
        if lastread is not None:
            data['lastread'] = lastread.chapter
            data['bookmarked'] = Bookmarked.objects.filter(author=request.user,book_id=pk).exists()
    else:
        data['bookmarked'] = False
    return render(request, 'book.html', data)


def topRated(request,page):
    data = {'sorttype': 'Books By Rating', 'books': bookbyrating(page)}
    return render(request, 'listing.html', data)


def popularBooks(request,page):
    data = {'sorttype': 'Rising Books', 'books': bookrisingpop(page)}
    return render(request, 'listing.html', data)


def newBooks(request,page):
    data = {'sorttype': 'New Books', 'books': bookbynew(page)}
    return render(request, 'listing.html', data)


def userpage(request):
    if not request.user.is_authenticated:
        return 'uh oh stinky'
    data = {'user': request.user, 'books': bookbyauthor(request.user), 'reviews': reviewbyuser(request.user), }
    return render(request, 'userpage.html', data)


def chapterpage(request,pk,page):
    data = {'chapter': Chapter.objects.get(pk=pk).select_related(), 'comments':commentspage(pk,page)}


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def bookmark(request):
    if 'bookid' not in request.POST:
        return redirect("/")
    if request.user.is_authenticated:
        bookmarkSWITCH(request,request.POST['bookid'])
    return redirect(f"book/{request.POST['bookid']}/")

def createReview(request):
    if 'bookid' not in request.POST:
        return redirect("/")
    if request.user.is_authenticated:
        reviewPOST(request,request.POST['bookid'])
    return redirect(f"book/{request.POST['bookid']}/")