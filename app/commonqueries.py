import datetime

from app.models import Book, Review


def bookbyrating(page=1,total=20):
    return Book.objects.order_by('-scoretotal/reviewcount')[(page - 1) * total:page * total]

def bookrisingpop(page=1,total=20):
    twoweeksago = datetime.now() - datetime.timedelta(days=14)
    reviews = Review.objects.filter(release__gt=twoweeksago).select_related('novel').aggregate()

    novels = {}
    for review in reviews: #basic mapping-by-score, maybe I could've done this on db?
        if review.novel in novels.keys():
            novels[review.novel]+= review.rating
        else:
            novels[review.novel] = review.rating

    return sorted(novels.keys(), key=lambda x: -novels[x])[(page - 1) * total:page * total]

def bookbynew(page=1, total=20):
    return Book.objects.reverse()[(page - 1) * total:page * total]