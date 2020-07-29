from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, "index.html")
    # return HttpResponse("<h1>Welcome to Hotel Website</h1>")


def createuser(request):
    return render(request, "signup.html")


def showaboutus(request):
    return render(request, "aboutus.html")
