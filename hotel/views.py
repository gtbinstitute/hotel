from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

from .models import RoomCategory, RoomCategoryDetails
from .forms import SignupForm, LoginForm, BookingForm


def index(request):
    return render(request, "index.html")
    # return HttpResponse("<h1>Welcome to Hotel Website</h1>")


def AllRooms(request):
    obj = RoomCategory.objects.all()  # Getting all the records from database
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


def useraccount(request):
    return render(request, "myaccount.html")


def mylogin(request):
    formobj = LoginForm(request.POST or None)
    if formobj.is_valid():
        username = formobj.cleaned_data.get("username")
        userobj = User.objects.get(username__iexact=username)
        login(request, userobj)
        request.session["myusername"] = userobj.username
        request.session["myuseremail"] = userobj.email
        # request.session["joineddate"] = userobj.date_joined
        return HttpResponseRedirect(reverse("ghar"))
    else:
        return render(request, "login.html", {"form": formobj})


@login_required
def booking(request):
    formobj = BookingForm(request.POST or None)
    if formobj.is_valid():
        pass
    else:
        pass
    return render(request, "booking.html", {"form": formobj})



@login_required
def changepassword(request):
    if request.method == 'POST':
        data = request.POST
        oldpassword = data.get("oldpassword", "1")
        password1 = data.get("password1", "0")
        password2 = data.get("password2", "0")
        if password1 == password2:
            myusername = request.session["myusername"]
            userobj = authenticate(username=myusername, password=oldpassword)
            if userobj:
                userobj.set_password(password1)
                userobj.save()
                logout(request)
                formobj = LoginForm(None)
                context = {"form": formobj, "loginmessage": "done"}
                return render(request, "login.html", context)
            else:
                context = {"mymessage": "Wrong old password"}
        else:
            context = {"mymessage": "New Passwords does not match"}
        return render(request, "changepassword.html", context)
    else:
        return render(request, "changepassword.html")


def mysignout(request):
    if request.session.has_key("myusername"):
        del request.session["myusername"]
        logout(request)
        return HttpResponseRedirect(reverse("ghar"))


def showaboutus(request):
    return render(request, "aboutus.html")
