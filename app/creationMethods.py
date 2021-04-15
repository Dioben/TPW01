from django.http import HttpResponse

from models import *
def booksPOST(book):
    pass


def chapterPOST(chapter):
    pass


def bookmarkPOST(request,bookid):
    #if user.auth'd
    bookmark = Bookmarked(author=request.user, book_id=bookid)
    bookmark.save()
    return HttpResponse(bookmark, status=201)


def reviewPOST(request):
    pass
    #TODO: IF NEW REVIEW MESS WITH BOOK RATING/REVIEWS
    #IF NOT NEW JUST MESS WITH RATING BY SUBSTRACTING FORMER VALUE AND ADDING NEW


def advanceReadingStatus(request,book,chapter):
    #if user.auth'd
    try:
        lastread = LastRead.objects.get(author=request.user, book_id=book)
        lastread.chapter_id = chapter
    except:
        lastread = LastRead(author=request.user,book_id=book, chapter_id=chapter)
    lastread.save()
    return HttpResponse(lastread, status=201)
