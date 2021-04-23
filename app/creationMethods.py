from django.db.models import F
from django.http import HttpResponse

from app.forms import ReviewForm
from app.models import *
def booksPOST(book):
    pass


def chapterPOST(chapter):
    pass


def bookmarkPOST(request,bookid):#NOTE: BOOKMARK METHODS DO NOT TEST AUTH, DO THAT IN PARENT METHOD
    bookmark = Bookmarked(author=request.user, book_id=bookid)
    bookmark.save()
    return HttpResponse(bookmark, status=201)

def bookmarkDELETE(request,bookid):
    bookmark = Bookmarked.objects.filter(author=request.user, book_id=bookid)
    if bookmark.exists():
        bookmark.delete()
        return HttpResponse(bookmark,status=202)
    return HttpResponse("",status=204)

def bookmarkSWITCH(request,bookid): #ONLY USING THIS ONE, OTHERS ARE AROUND FOR REST API IMPLEMENTATION PURPOSES, CONSIDER REMOVING
    bookmark = Bookmarked.objects.filter(author=request.user, book_id=bookid)
    if bookmark.exists():
        bookmark.delete()
        return HttpResponse(bookmark, status=202)
    bookmark = Bookmarked(author=request.user,book_id=bookid)
    bookmark.save()
    return HttpResponse(bookmark, status=201)

def reviewPOST(request):
    reviewform = ReviewForm(request.POST)
    if not reviewform.is_valid():
        return
    review = Review.objects.filter(author=request.user,novel_id=reviewform.novel)
    if review.exists():
        review = review.get()
        Book.objects.filter(pk=reviewform.novel).update(scoretotal=F('scoretotal')-review.rating+reviewform.rating)
        review.rating = reviewform.rating
        review.text = reviewform.cleaned_data['text']
    else:
        review = reviewform.save(commit=False)
        review.author = request.user
        Book.objects.filter(pk=reviewform.novel).update(scoretotal=F('scoretotal') + review.rating,reviewcount=F('reviewcount')+1)
    review.save()


def advanceReadingStatus(request,book,chapter):
    if request.user.is_authenticated:
        # noinspection PyBroadException
        try:
            lastread = LastRead.objects.get(author=request.user, book_id=book)
            lastread.chapter_id = chapter
        except:
            lastread = LastRead(author=request.user,book_id=book, chapter_id=chapter)
        lastread.save()
        return HttpResponse(lastread, status=201)
