from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from .models import RoomCategory, RoomCategoryDetails
from .forms import SignupForm, LoginForm


def index(request):
    return render(request, "index.html")
    # return HttpResponse("<h1>Welcome to Hotel Website</h1>")

def AllRooms(request):
    obj = RoomCategory.objects.all()    #Getting all the records from database
    context = {"roomdetails": obj}
    return render(request, "rooms.html", context)

def RoomDetails(request, catid):
    obj = RoomCategoryDetails.objects.select_related('roomcategoryid').filter(roomcategoryid=catid)
    obj2 = RoomCategoryDetails.objects.select_related('roomcategoryid').filter(roomcategoryid=catid).first()
    context = {"roomcategorydetails": obj, "roomcatdetails": obj2}
    return render(request, "roomdetails.html", context)

class createuser(SuccessMessageMixin, CreateView):
    form_class = SignupForm
    template_name = 'signup.html'
    success_message = "Your account has been created successfully"
    success_url = reverse_lazy('signup')

    def dispatch(self, *args, **kwargs):
        return super(createuser, self).dispatch(*args, **kwargs)

def mylogin(request):
    formobj = LoginForm(request.POST or None)
    if formobj.is_valid():
        username = formobj.cleaned_data.get("username")
        userobj = User.objects.get(username__iexact=username)
        login(request, userobj)
        request.session["myusername"] = userobj.username
        request.session["myuseremail"] = userobj.email
        return HttpResponseRedirect(reverse("ghar"))
    else:
        return render(request, "login.html", {"form": formobj})

def mysignout(request):
    if request.session.has_key("myusername"):
        del request.session["myusername"]
        logout(request)
        return HttpResponseRedirect(reverse("ghar"))

def showaboutus(request):
    return render(request, "aboutus.html")