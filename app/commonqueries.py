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
    '''
    novels = {}
    for review in reviews: #basic mapping-by-score, maybe I could've done this on db?
        if review.novel in novels.keys():
            novels[review.novel]+= review.rating
        else:
            novels[review.novel] = review.rating
    '''
    data = {review.novel for review in reviews[(page - 1) * total:page * total]}
    for novel in data:
        novel.rating = novel.scoretotal/novel.reviewcount
        if novel.reviewcount == 0:
            novel.rating = 'fuck you'
    print(data)
    return data


def bookbynew(page=1, total=20):
    return Book.objects.reverse()[(page - 1) * total:page * total]


def reviewbyuser(user):
    return Review.objects.filter(author=user)


def commentspage(chapter,page=1, total=15):
    comments = Comment.objects.filter(chapter_id=chapter,parent__comment=None).select_related("author")[(page - 1) * total:page * total]
    childcomments = Comment.objects.filter(parent__comment__in=comments).select_related("author")
    return list(chain(comments,childcomments))