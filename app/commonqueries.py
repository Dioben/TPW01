import datetime
from itertools import chain

from django.db.models import Count, Sum, F
from app.models import *
from django.utils import timezone


def bookbyauthor(author):
    return Book.objects.filter(author=author)


def bookbyrating(page=1, total=20):
    return Book.objects.annotate(rating=F('scoretotal')/F('reviewcount')).order_by('-rating')[(page - 1) * total:page * total]


def bookrisingpop(page=1, total=20):
    twoweeksago = timezone.now() - timezone.timedelta(days=14)
    reviews = Review.objects.filter(release__gt=twoweeksago).select_related('novel').annotate(popularity=1/Count('novel')*Sum('rating'),).order_by('-popularity')
    data = list(dict.fromkeys(review.novel for review in reviews))[(page - 1) * total:page * total]
    for novel in data:
        if novel.reviewcount == 0:
            novel.rating = 0
        else:
            novel.rating = round(novel.scoretotal/novel.reviewcount)
    return data


def bookbynew(page=1, total=20):
    return Chapter.objects.order_by("-release").select_related()[(page - 1) * total:page * total]


def reviewbyuser(user):
    return Review.objects.filter(author=user)


def commentspage(chapter,page=1, total=15):
    comments = Comment.objects.filter(chapter_id=chapter,parent__comment=None)[(page - 1) * total:page * total]
    parents = [item['id'] for item in comments.values()]
    childcomments = Comment.objects.filter(parent__in=parents)
    return list(chain(comments,childcomments))


def reviewpage(book,page=1,total=25):
    return Review.objects.filter(novel=book)[(page - 1) * total:page * total]


def bookmarksbyuser(user):
    return Book.objects.filter(bookmarks=user)


def bookbytitle(title, page=1, total=20):
    return Book.objects.filter(title__contains=title).annotate(rating=F('scoretotal')/F('reviewcount')).order_by('title')[(page - 1) * total:page * total]
