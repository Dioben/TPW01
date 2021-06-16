import math

from django.contrib.auth import authenticate, login
from django.db import transaction
from django.shortcuts import render, redirect

from app.commonqueries import *
from app.creationMethods import *
from app.forms import ChapterPostForm, BookCreationForm, CommentForm, CustomUserCreationForm
from app.models import *

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import *
# Create your views here.



COMMENTSPERPAGE = 15
REVIEWSPERPAGE = 10
BOOKSPERPAGE = 15

# HOME PAGE
def index(request):
    data = {'newchaps': Chapter.objects.order_by("-release").select_related()[:5], 'toprated': bookbyrating(total=5),
            'rising': bookrisingpop(total=5)}
    return render(request, "index.html", data)


def bookpage(request, pk,page):
    data = {'book': Book.objects.select_related().get(pk=pk), 'lastread': 0, 'isauthor': False ,'page':page,'nextpage':page+1}
    data['chapters'] = Chapter.objects.only("title", "number", "release").filter(novel=data['book'])
    data['reviews'] = reviewpage(data['book'],page,REVIEWSPERPAGE)
    data['rating'] = str(round(0 if data['book'].reviewcount == 0 else data['book'].scoretotal/data['book'].reviewcount, 1))
    pages = Review.objects.filter(novel_id=pk).count() / REVIEWSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    data['maxpages'] = pages
    data['secondtolast'] = pages-1
    if request.user.is_authenticated:
        possiblereview = Review.objects.filter(author=request.user, novel_id=pk)
        data['isauthor'] = request.user == data['book'].author
        if possiblereview.exists():
            data['form'] = ReviewForm(instance=possiblereview.get(),initial={'novel':pk})
            data['userreviewid'] = possiblereview.get().id
        else:
            data['form'] = ReviewForm(initial={'novel': pk})  # do not render this if author or nonauth'd
        lastread = LastRead.objects.filter(book_id=pk, author=request.user)
        if lastread.exists():
            data['lastread'] = lastread.get().chapter.number
        data['bookmarked'] = Book.objects.filter(pk=pk, bookmarks=request.user).exists()
    else:
        data['bookmarked'] = False
    return render(request, 'book.html', data)


def topRated(request, page):
    data = {'sorttype': 'Top Books', 'books': bookbyrating(page,BOOKSPERPAGE), 'next': page + 1, 'previous': page - 1, 'page':page, 'urlprefix':'top'}
    pages = Book.objects.all().count() / BOOKSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    data['maxpages'] = pages
    data['secondtolast'] = pages - 1
    return render(request, 'listing.html', data)


def popularBooks(request, page):
    data = {'sorttype': 'Rising Books', 'books': bookrisingpop(page,BOOKSPERPAGE), 'next': page + 1, 'previous': page - 1, 'page':page,'urlprefix':'hot'}
    twoweeksago = timezone.now() - timezone.timedelta(days=14)
    pages = len({x['novel'] for x in Review.objects.filter(release__gt=twoweeksago).values('novel')}) / BOOKSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    data['maxpages'] = pages
    data['secondtolast'] = pages - 1
    return render(request, 'listing.html', data)


def newBooks(request, page):
    data = {'sorttype': 'Latest Books', 'books': bookbynew(page,BOOKSPERPAGE), 'next': page + 1, 'previous': page - 1, 'page':page,'urlprefix':'new'}
    pages = Chapter.objects.all().count() / BOOKSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    data['maxpages'] = pages
    data['secondtolast'] = pages - 1
    return render(request, 'listing.html', data)


def userpage(request):
    if not request.user.is_authenticated:
        return HttpResponse('You are not signed in', 403)
    data = {'acc_owner': request.user, 'books': bookbyauthor(request.user), 'bookmarks': bookmarksbyuser(request.user)} #, 'reviews': reviewbyuser(request.user)}
    return render(request, 'user.html', data)


def chapterpage(request, book, number, page):
    chapter = Chapter.objects.get(novel_id=book, number=number)
    book = chapter.novel
    author = book.author
    form = CommentForm()
    if request.user.is_authenticated:
        lastread = LastRead.objects.filter(book_id=book, author=request.user)
        if lastread.exists():
            lastread = lastread.get()
            lastread.chapter = chapter
            lastread.save()
        else:
            lastread = LastRead(author=request.user, book=book, chapter=chapter)
            lastread.save()
    form.chapter = chapter
    pages = Comment.objects.filter(chapter_id=chapter.id,parent__chapter=None).count() / COMMENTSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    data = {'chapter': chapter, 'book': book, 'author': author,
            'comments': commentspage(chapter.id, page, COMMENTSPERPAGE),
            'isauthor': author == request.user, 'next': chapter.number + 1, 'previous': chapter.number - 1,
            'form': form, 'page': page, 'maxpage': pages, 'secondtolast': pages - 1}
    return render(request, 'chapter.html', data)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def bookmark(request):
    if 'bookid' not in request.POST:
        return redirect("/")
    if request.user.is_authenticated:
        bookmarkSWITCH(request, request.POST['bookid'])
    return redirect(f"/book/{request.POST['bookid']}/")


def createReview(request):
    if request.user.is_authenticated:
        reviewPOST(request)
    return redirect(f"/book/{request.POST['novel']}/")


def chaptereditor(request, book, chapter):
    novel = Book.objects.get(pk=book)
    if not (request.user.is_authenticated and novel.author == request.user):
        return HttpResponse("You are not the author", 403)
    if chapter == "new":
        form = ChapterPostForm(initial={'novel':book})
        chapter = 0
    else:
        chap = Chapter.objects.get(number=int(chapter), novel=novel)
        form = ChapterPostForm(instance=chap, initial={'novel':book})
    data = {'book': novel, 'form': form, 'chapter_id': chapter}
    return render(request, "chaptereditor.html", data)


def bookEditor(request, book):  # book=0 if new?
    if not request.user.is_authenticated:
        return HttpResponse('Log in first', 403)
    novel = Book.objects.filter(pk=book)
    if novel.exists():
        novel = novel.get()
        if novel.author != request.user:
            return HttpResponse('You are not the author', 403)
    else:
        novel = Book(author=request.user)
    form = BookCreationForm(instance=novel)
    return render(request, "bookeditor.html", {'bookid': book, 'form': form})


def deletebook(request, book):
    novel = Book.objects.get(pk=book)
    if not request.user.is_authenticated or not (request.user.is_staff or request.user == novel.author):
        return HttpResponse('Forbidden', 403)
    novel.delete()
    return redirect('/')


def submitbook(request, book):
    if not request.user.is_authenticated:
        return HttpResponse('Log in First', 403)
    novel = Book.objects.filter(pk=book)
    if not novel.exists():
        novel = Book(author=request.user)
    else:
        novel = novel.get()
    if request.user != novel.author:
        return HttpResponse('Access forbidden', 403)
    form = BookCreationForm(request.POST)
    if form.is_valid():
        novel.title = form.cleaned_data['title']
        novel.description = form.cleaned_data['description']
        novel.save()
        return redirect(f'/book/{novel.id}')
    else:
        return render(request, "bookeditor.html", {'bookid': book, 'form': form})


def submitchapter(request, chapterid):
    if not request.user.is_authenticated or 'novel' not in request.POST:
        return HttpResponse('Log in first', 403)
    chapter = Chapter.objects.filter(pk=chapterid)
    if chapter.exists():
        chapter = chapter.get()
    else:
        chapter = Chapter()
        chapterid = 0
    form = ChapterPostForm(request.POST)
    if form.is_valid():
        if Book.objects.get(pk=form.cleaned_data['novel']).author != request.user:
            return HttpResponse('Unauthorized author', 403)
        chapter.novel = Book.objects.get(pk=form.cleaned_data['novel'])
        chapter.title = form.cleaned_data['title']
        chapter.text = form.cleaned_data['text']
        chaptersubmittransaction(chapterid, chapter)
        return redirect(f'/book/{form.cleaned_data["novel"]}')
    else:
        data = {'chapter_id': chapterid, 'book': Book.objects.get(pk=request.POST['novel']).id, 'form': form}
        return render(request, "chaptereditor.html", data)


@transaction.atomic
def chaptersubmittransaction(chid, chapter):
    if not chid:  # new chapter
        chapter.novel.chapters += 1
        chapter.number = chapter.novel.chapters
        chapter.novel.save()
    chapter.save()


def deletechapter(request, chapterid):
    if not request.user.is_authenticated:
        return HttpResponse('Log in First', 403)
    chapter = Chapter.objects.filter(pk=chapterid)
    if chapter.exists():
        chapter = chapter.get()
        if request.user.is_staff or chapter.novel.author == request.user:
            nv = chapter.novel
            chapterdeletetransaction(chapter)

            return redirect(f'/book/{nv.id}')
        return HttpResponse("No permission", 403)
    else:
        return HttpResponse("Not Found", 404)


@transaction.atomic
def chapterdeletetransaction(chapter):
    Chapter.objects.filter(novel=chapter.novel, number__gt=chapter.number).update(number=F('number') - 1)
    chapter.novel.chapters -= 1
    chapter.novel.save()
    chapter.delete()


def chapterentry(request, book, number):
    return redirect(f'1/')


def postcomment(request):
    if not request.user.is_authenticated:
        return HttpResponse("no account", 403)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = Comment(author=request.user, content=form.cleaned_data['content'], chapter=form.cleaned_data['chapter'])
        if 'parent' in request.POST:
            comment.parent = Comment.objects.get(pk=request.POST['parent'])
        comment.save()
        return redirect(f'/chapter/{request.POST["book"]}/{request.POST["chapternumber"]}/{request.POST["page"]}')
    return HttpResponse("something went wrong", 404)


def deletecomment(request, pk):
    if not request.user.is_authenticated:
        return HttpResponse("Please log in", 403)
    comment = Comment.objects.filter(pk=pk)
    if not comment.exists():
        return HttpResponse("Comment not found",404)
    comment = comment.get()
    if comment.author != request.user and not request.user.is_staff:
        return HttpResponse("No delete permissions",403)
    backurl = f'/chapter/{comment.chapter.novel.id}/{comment.chapter.number}/1/'
    comment.delete()
    return redirect(backurl)


def bookredir(request,pk):
    return redirect(f'1/')


def deletereview(request,pk):
    if not request.user.is_authenticated:
        return HttpResponse("Please log in", 403)
    review = Review.objects.filter(pk=pk)
    if not review.exists():
        return HttpResponse("Review not found",404)
    review = review.get()
    if review.author != request.user and not request.user.is_staff:
        return HttpResponse("No delete permissions",403)
    backurl = f'/book/{review.novel.id}/'
    reviewdeletetransaction(review)
    return redirect(backurl)


@transaction.atomic
def reviewdeletetransaction(review):
    Book.objects.filter(pk=review.novel.id).update(scoretotal=F('scoretotal') - review.rating, reviewcount=F('reviewcount') - 1)
    review.delete()


def search(request, page):
    if 'title' not in request.GET:
        return redirect('/')
    data = {
        'sorttype': 'Search results',
        'books': bookbytitle(request.GET['title'], page, BOOKSPERPAGE),
        'next': page + 1,
        'previous': page - 1,
        'page': page,
        'urlprefix': 'search',
        'search': request.GET['title']
    }
    pages = Book.objects.filter(title__contains=request.GET['title']).count() / BOOKSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    data['maxpages'] = pages
    data['secondtolast'] = pages - 1
    return render(request, 'listing.html', data)


@api_view(['GET'])
def apiPopularBooks(request,page):
    books = bookrisingpop(page, BOOKSPERPAGE)
    twoweeksago = timezone.now() - timezone.timedelta(days=14)
    pages = len({x['novel'] for x in Review.objects.filter(release__gt=twoweeksago).values('novel')}) / BOOKSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    serializer = BookSerializer(books, many=True)

    return Response({'books':serializer.data, 'pages':pages})

@api_view(['GET'])
def apiNewBooks(request,page):
    chapters = bookbynew(page, BOOKSPERPAGE)
    pages = Chapter.objects.all().count() / BOOKSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    serializer = ChapterSerializer(chapters, many=True)
    return Response({'chapters':serializer.data, 'pages':pages})

@api_view(['GET'])
def apiTopRated(request, page):
    books = bookbyrating(page, BOOKSPERPAGE)
    pages = Book.objects.all().count() / BOOKSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    serializer = BookSerializer(books, many=True)
    return Response({'books': serializer.data, 'pages': pages})

@api_view(['GET'])
def apiProfile(request):
    if not request.user.is_authenticated:
        return Response('You are not signed in', 403)
    userSerializer = UserSerializer(request.user)
    bookSerializer = BookSerializer(bookbyauthor(request.user), many=True)
    bookmarks =BookSerializer(bookmarksbyuser(request.user), many=True)
    data = {'acc_owner': userSerializer.data, 'books': bookSerializer.data, 'bookmarks': bookmarks.data }
    return Response(data)

@api_view(['GET'])
def apiBookpage(request,pk):
    data = {}
    try:
        book = BookSerializer(Book.objects.get(pk=pk))
        data['book'] = book.data
    except Book.DoesNotExist:
        return Response("Content Not Found", 404)
    if request.user.is_authenticated:
        possiblereview = Review.objects.filter(author=request.user, novel_id=pk)
        if possiblereview.exists():
            self_review = ReviewSerializer(possiblereview.get())
            data['self_review'] = self_review.data
        lastread = LastRead.objects.filter(book_id=pk, author=request.user)
        if lastread.exists():
            data['lastread'] = lastread.get().chapter.number
        else:
            data['lastread'] = 0
        data['bookmarked'] = Book.objects.filter(pk=pk, bookmarks=request.user).exists()
    else:
        data['lastread']=0
        data['bookmarked'] = False

    chapters = SimpleChapterSerializer(Chapter.objects.only("title", "number", "release").filter(novel=pk),many=True)
    data['chapters'] = chapters.data
    reviews = ReviewSerializer(reviewpage(pk, 1, REVIEWSPERPAGE), many=True)
    data['reviews'] = reviews.data
    data['rating'] = str(
        round(0 if data['book']['reviewcount'] == 0 else data['book']['scoretotal'] / data['book']['reviewcount'], 1))
    pages = Review.objects.filter(novel_id=pk).count() / REVIEWSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    data['pages'] = pages
    return Response(data)

@api_view(['GET'])
def apiReviews(request, book, page):
    try:
        book = Book.objects.get(pk=book)
    except Book.DoesNotExist:
        return Response("Content Not Found", 404)
    reviews = ReviewSerializer(reviewpage(book, page, REVIEWSPERPAGE), many=True)
    return Response(reviews.data)

@api_view(['GET'])
def apiChapterpage(request,book,number):
    data = {}
    try:
        chapter = Chapter.objects.get(novel_id=book, number=number)
    except Chapter.DoesNotExist:
        return Response("Content Not Found", 404)
    author = UserSerializer(chapter.novel.author)
    data['author'] = author.data

    if request.user.is_authenticated:
        lastread = LastRead.objects.filter(book_id=book, author=request.user)
        if lastread.exists():
            lastread = lastread.get()
            lastread.chapter = chapter
            lastread.save()
        else:
            lastread = LastRead(author=request.user, book=chapter.novel, chapter=chapter)
            lastread.save()
    chapter = ChapterSerializer(chapter)
    pages = Comment.objects.filter(chapter_id=chapter.data['id'], parent__chapter=None).count() / COMMENTSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    data['pages'] = pages
    comments = CommentSerializer(commentspage(chapter.data['id'], 1, COMMENTSPERPAGE), many=True)
    data['comments'] = comments.data
    data['chapter'] = chapter.data
    return Response(data)

@api_view(['GET'])
def apiComments(request,chapter,page):
    try:
        comments = CommentSerializer(commentspage(chapter,page,COMMENTSPERPAGE),many=True)
    except Book.DoesNotExist:
        return Response("Content Not Found", 404)
    return Response(comments.data)

@api_view(['GET'])
def apiBookmark(request,book):
    if not request.user.is_authenticated:
        return Response("Please Log in", 403)
    try:
        book = Book.objects.get(pk=book)
    except:
        return Response("Content Not Found", 404)
    if Book.objects.filter(pk=book.id, bookmarks=request.user).exists():
        book.bookmarks.remove(request.user)
        return Response({"bookmarked": False})
    book.bookmarks.add(request.user)
    book.save()
    return Response({"bookmarked": True})

@api_view(['PUT'])
def apiBookEditor(request):
    id = request.data['id']
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        book = Book.objects.get(pk=id)
    except Book.DoesNotExist:
        return Response("Content Not Found", status=404)
    if book.author!=request.user:
        return Response("You do not have permission to do this", 403)
    serializer = BookSerializer(book,data=request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response("Bad Format", 400)
    return Response(serializer.data)

@api_view(['POST'])
def apiSubmitbook(request):
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()
        book.author = request.user
        book.save()
    else:
        return Response("Bad Format", 400)
    serializer = BookSerializer(book)
    return Response(serializer.data,201)

@api_view(['DELETE'])
def apiDeletebook(request, book):
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        book = Book.objects.get(pk=book)
    except Book.DoesNotExist:
        return Response("Content Not Found", status=404)
    if book.author != request.user:
        return Response("You do not have permission to do this", 403)
    book.delete()
    return Response(status=204)

@api_view(['POST'])
def apiSubmitchapter(request):
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    serializer = ChapterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response("Bad Format", 400)
    try:
        book = Book.objects.get(pk=request.data['novel'])
    except Book.DoesNotExist:
        return Response("Content Not Found", status=404)
    if book.author != request.user:
        return Response("You do not have permission to do this", 403)
    serializer.save()
    return Response(serializer.data, 201)

@api_view(['PUT'])
def apiChapterEdit(request):
    id = request.data['id']
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        chapter = Chapter.objects.get(pk=id)
    except Chapter.DoesNotExist:
        return Response("Content Not Found", status=404)
    book = chapter.novel
    if book.author != request.user:
        return Response("You do not have permission to do this", 403)
    serializer = ChapterSerializer(chapter,data=request.data)
    if not serializer.is_valid():
        return Response("Bad Format", 400)
    serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def apiDeletechapter(request,chapterid):
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        chapter = Chapter.objects.get(pk=chapterid)
    except Chapter.DoesNotExist:
        return Response("Content Not Found", status=404)
    book = chapter.novel
    if book.author != request.user:
        return Response("You do not have permission to do this", 403)
    chapter.delete()
    return Response(status=204)

@api_view(['GET'])
def apiSearch(request,query,page):
    books = bookbytitle(query,page,BOOKSPERPAGE)
    pages = Book.objects.filter(title__contains=request.GET['title']).count() / BOOKSPERPAGE
    if pages:
        if math.modf(pages)[0]:  # if not perfect division
            pages += 1
        pages = int(pages)
    else:
        pages = 1
    serializer = BookSerializer(books, many=True)
    contentdict = serializer.data
    contentdict['pages'] = pages
    return Response(contentdict)

@api_view(['POST'])
def apiPostcomment(request):
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        chapter = Chapter.objects.get(pk=request.data['chapter'])
    except Chapter.DoesNotExist:
        return Response("Content Not Found", status=404)
    serializer = CommentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response("Bad Format", 400)
    else:
        comment = serializer.save()
        comment.author = request.user
        comment.save()
    return Response(serializer.data,201)

@api_view(['PUT'])
def apiEditcomment(request):
    id = request.data['id']
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        comment = Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        return Response("Content Not Found", status=404)
    serializer = CommentSerializer(comment,data=request.data)
    if not serializer.is_valid():
        return Response("Bad Format", 400)
    comment.content = serializer.data['content']
    comment.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def apiDeletecomment(request):
    id = request.data['id']
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        comment = Comment.objects.get(pk=id)
    except Comment.DoesNotExist:
        return Response("Content Not Found", status=404)
    if comment.author != request.user:
        return Response("You do not have permission to do this", 403)
    comment.delete()
    return Response(status=204)

@api_view(['POST'])
def apiCreateReview(request):
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        book = Book.objects.get(pk=request.data['novel'])
    except Book.DoesNotExist:
        return Response("Content Not Found", status=404)
    serializer = ReviewSerializer(data=request.data)
    if not serializer.is_valid():
        return Response("Bad Format", 400)
    if Review.objects.filter(author=request.user,novel=book).exists:
        review = Review.objects.get(author=request.user,novel=book)
        review.rating = serializer.data['rating']
        review.text = serializer.data['text']
    else:
        review = serializer.save()
        review.author = request.user
    review.save()

@api_view(['DELETE'])
def apiDeletereview(request,book):
    if not request.user.is_authenticated:
        return Response("Please Log In", 403)
    try:
        review = Review.objects.get(novel_id=book, author=request.user)
    except Review.DoesNotExist:
        return Response("Content Not Found", status=404)
    review.delete()
    return Response(status=204)