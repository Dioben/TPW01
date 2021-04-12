from django.shortcuts import render
from models import *
# Create your views here.

#HOME PAGE
#TODO: put something in index.html/index.js, load latest chapters and top rated fics onto frontpage
#  REST STUFF SHOULD BE IN DIFFERENT FILES, MAKE FILES FOR GET,POST AND DELETE POSSIBLY
def index(request):
    data = {}
    return render(request, "index.html", data)


def latest(request):
    return Chapter.objects.reverse()[:20] #hopefully the last 20 chapters with books attached


def popular(request):
    return Book.objects.order_by("scoretotal/reviewcount") #unsure whether this works, just needs to be the books



