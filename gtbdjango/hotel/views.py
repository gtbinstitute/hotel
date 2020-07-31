from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from gtbdjango.hotel.forms import SignupForm


def index(request):
    return render(request, "index.html")
    # return HttpResponse("<h1>Welcome to Hotel Website</h1>")


class createuser(SuccessMessageMixin, CreateView):
    form_class = SignupForm
    template_name = 'signup.html'
    success_message = "Your account has been created successfully"
    success_url = reverse_lazy('signup')

    def dispatch(self, *args, **kwargs):
        return super(createuser, self).dispatch(*args, **kwargs)


def showaboutus(request):
    return render(request, "aboutus.html")
