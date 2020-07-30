from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from django.views.generic import CreateView

from gtbdjango.hotel.forms import SignupForm


def index(request):
    return render(request, "index.html")
    # return HttpResponse("<h1>Welcome to Hotel Website</h1>")


class createuser(CreateView):
    form_class = SignupForm
    template_name = 'signup.html'


def showaboutus(request):
    return render(request, "aboutus.html")
