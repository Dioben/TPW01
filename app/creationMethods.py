from django.db.models import F
from django.http import HttpResponse

from models import *
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

def reviewPOST(request,bookid):
    review = Review.objects.filter(author=request.user,novel_id=bookid)
    if review.exists():
        review = review.get()
        Book.objects.filter(pk=bookid).update(scoretotal=F('scoretotal')-review.rating+request.post['rating'])
        review.rating = request.post['rating']#TODO: SWAP ATTRIBUTIONS HERE, MOVE TO FORMS
    else:

    #TODO: IF NEW REVIEW MESS WITH BOOK RATING/REVIEWS
    #IF NOT NEW JUST MESS WITH RATING BY SUBSTRACTING FORMER VALUE AND ADDING NEW


def advanceReadingStatus(request,book,chapter):
    if request.user.is_authenticated:
        try:
            lastread = LastRead.objects.get(author=request.user, book_id=book)
            lastread.chapter_id = chapter
        except:
            lastread = LastRead(author=request.user,book_id=book, chapter_id=chapter)
        lastread.save()
        return HttpResponse(lastread, status=201)
