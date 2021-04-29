from django.db import transaction
from django.db.models import F
from django.http import HttpResponse

from app.forms import ReviewForm
from app.models import *


def bookmarkPOST(request, bookid):  # NOTE: BOOKMARK METHODS DO NOT TEST AUTH, DO THAT IN PARENT METHOD
    book = Book.objects.get(pk=bookid)
    book.bookmarks.add(request.user)
    book.save()
    return HttpResponse(book, status=201)


def bookmarkDELETE(request, bookid):
    book = Book.objects.get(pk=bookid)
    if Book.objects.filter(pk=bookid, bookmarks=request.user).exists():
        book.bookmarks.remove(request.user)
        return HttpResponse(book, status=202)
    return HttpResponse("", status=204)


def bookmarkSWITCH(request, bookid):  # ONLY USING THIS ONE, OTHERS ARE AROUND FOR REST API IMPLEMENTATION PURPOSES, CONSIDER REMOVING
    book = Book.objects.get(pk=bookid)
    if Book.objects.filter(pk=bookid, bookmarks=request.user).exists():
        book.bookmarks.remove(request.user)
        return  # HttpResponse(bookmark, status=202)
    book.bookmarks.add(request.user)
    book.save()
    return  # HttpResponse(bookmark, status=201)


@transaction.atomic
def reviewPOST(request):
    reviewform = ReviewForm(request.POST)
    if not reviewform.is_valid():
        return
    review = Review.objects.filter(author=request.user, novel_id=reviewform.cleaned_data['novel'])
    book = Book.objects.filter(pk=reviewform.cleaned_data['novel'])
    if not book.exists():
        return
    if review.exists():
        review = review.get()
        book.update(scoretotal=F('scoretotal') - review.rating + reviewform.cleaned_data['rating'])
        review.rating = reviewform.cleaned_data['rating']
        review.text = reviewform.cleaned_data['text']
    else:
        review = reviewform.save(commit=False)
        review.author = request.user
        review.novel = book.get()
        book.update(scoretotal=F('scoretotal') + review.rating,reviewcount=F('reviewcount') + 1)
    review.save()


def advanceReadingStatus(request, book, chapter):
    if request.user.is_authenticated:
        # noinspection PyBroadException
        try:
            lastread = LastRead.objects.get(author=request.user, book_id=book)
            lastread.chapter_id = chapter
        except:
            lastread = LastRead(author=request.user, book_id=book, chapter_id=chapter)
        lastread.save()
        return  # HttpResponse(lastread, status=201)
