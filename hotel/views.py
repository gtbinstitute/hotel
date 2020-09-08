import datetime

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
import requests
from django.core.mail import send_mail
from django.db import transaction

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, ListView, UpdateView

from hotel.token_generator import account_activation_token
from .models import RoomCategory, RoomCategoryDetails, Booking
from .forms import SignupForm, LoginForm, BookingForm, ProfileForm, UserForm, ContactForm


def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q=Jalandhar&appid=yourapikey&units=metric"
    json_data = requests.get(url).json()
    temperature = json_data["main"]["temp"]
    tempdata = {"temp": temperature}
    return render(request, "index.html", tempdata)
    # return HttpResponse("<h1>Welcome to Hotel Website</h1>")


def AllRooms(request):
    # obj2 = Booking.objects.filter(checkindate__lte=datetime.date.today())
    obj2 = RoomCategory.objects.all().order_by('-roomsavailable')
    # catname = obj2.categoryname
    # roomsavailable = str(obj2.roomsavailable)
    # obj = RoomCategory.objects.all()  # Getting all the records from database
    # context = {"catname1": catname, "roomsno" : roomsavailable}
    context = {"roomdetails": obj2}
    return render(request, "rooms.html", context)


def RoomDetails(request, catid):
    obj = RoomCategoryDetails.objects.select_related('roomcategoryid').filter(roomcategoryid=catid)
    obj2 = RoomCategoryDetails.objects.select_related('roomcategoryid').filter(roomcategoryid=catid).first()
    request.session["catid"] = catid
    # request.session["totalrooms"] = obj.roomcategoryid.roomsavailable
    context = {"roomcategorydetails": obj, "roomcatdetails": obj2}
    return render(request, "roomdetails.html", context)


class createuser(SuccessMessageMixin, CreateView):
    form_class = SignupForm
    template_name = 'signup.html'
    success_message = "Your account has been created but pending for authentication. Please check your mail to authenticate"
    success_url = reverse_lazy('signup')

    def dispatch(self, *args, **kwargs):
        return super(createuser, self).dispatch(*args, **kwargs)


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
@transaction.atomic
def updateuser(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')

        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'updateprofile.html', {'user_form': user_form, 'profile_form': profile_form})


def useraccount(request):
    return render(request, "myaccount.html")


def mylogin(request):
    formobj = LoginForm(request.POST or None)
    if formobj.is_valid():
        username = formobj.cleaned_data.get("username")
        userobj = User.objects.get(username__iexact=username)
        login(request, userobj)
        request.session["userid"] = userobj.id
        request.session["myusername"] = userobj.username
        request.session["myuseremail"] = userobj.email
        # request.session["joineddate"] = userobj.date_joined
        return HttpResponseRedirect(reverse("ghar"))
    else:
        return render(request, "login.html", {"sform": formobj})


@login_required
def booking(request, detailid):
    roomcategoryobj = RoomCategory.objects.get(id=request.session["catid"])
    roomcategorydetailsobj = RoomCategoryDetails.objects.get(id=detailid)
    image = roomcategoryobj.Image
    catname = roomcategoryobj.categoryname
    roomoptions = roomcategorydetailsobj.roomoptions
    details = {"image": image, "catname": catname, "roomoptions": roomoptions}
    formobj = BookingForm(request.POST or None)
    if request.method == "POST":
        if formobj.is_valid():
            data = formobj.save(commit=False)
            categoryid = request.session["catid"]

            case_1 = Booking.objects.filter(roomcategoryid=categoryid, checkindate__lte=data.checkindate,
                                            checkoutdate__gte=data.checkindate).exists()

            # case 2: a room is booked before the requested check_out date and check_out date is after requested
            # check_out date
            case_2 = Booking.objects.filter(roomcategoryid=categoryid, checkindate__lte=data.checkoutdate,
                                            checkoutdate__gte=data.checkoutdate).exists()

            case_3 = Booking.objects.filter(roomcategoryid=categoryid, checkindate__gte=data.checkindate,
                                            checkoutdate__lte=data.checkoutdate).exists()

            # if either of these is true, abort and render the error
            if case_1 or case_2 or case_3:
                count1 = Booking.objects.filter(roomcategoryid=categoryid, checkindate__lte=data.checkindate,
                                                checkoutdate__gte=data.checkindate).count()
                count2 = Booking.objects.filter(roomcategoryid=categoryid, checkindate__lte=data.checkoutdate,
                                                checkoutdate__gte=data.checkoutdate).count()
                count3 = Booking.objects.filter(roomcategoryid=categoryid, checkindate__gte=data.checkindate,
                                                checkoutdate__lte=data.checkoutdate).count()

                totalcount = 0
                if count1 > 0:
                    totalcount += count1
                elif count2 > 0:
                    totalcount += count2
                elif count3 > 0:
                    totalcount += count3

                if totalcount == roomcategoryobj.roomsavailable:
                    messages.error(request, 'Selected Dates are not available')
                    return render(request, "booking.html", {"form": formobj})

            data.userid = User(id=request.session["userid"])
            data.roomcategoryid = roomcategoryobj
            data.roomdetailid = RoomCategoryDetails(id=detailid)
            checkindate = data.checkindate
            checkoutdate = data.checkoutdate
            daysinfo = checkoutdate - checkindate

            data.amount = roomcategorydetailsobj.roomprice
            totalbill = data.amount * daysinfo.days

            data.save()

            bookingid = data.id

            messages.success(request,
                             'Your request for booking has been successful. Your booking id is ' + str(bookingid)
                             + ' Your total bill amount is ' + str(totalbill)
                             + '. Pay on 9834984938 on Google Pay / Paytm / UPI')
        else:
            formobj = BookingForm(request.POST)
    return render(request, "booking.html", {"form": formobj, "roomdetails": details})


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
        del request.session["userid"]
        logout(request)
    return HttpResponseRedirect(reverse("ghar"))


def showaboutus(request):
    return render(request, "aboutus.html")


def showcontactus(request):
    myform = ContactForm(request.POST or None)
    if myform.is_valid():
        data = request.POST
        name = data.get("name", "0")
        emailid = data.get("emailid", "0")
        message = data.get("message", "0")
        result = send_mail("Message from Hotel Website", "Name : " + name + "\nEmailid : " + emailid +
                           "\nMessage : " + message, "jalandhargtb@gmail.com", ["gtbcomputers@gmail.com"],
                           fail_silently=False)
        return render(request, "contactus.html", {"form": myform, "status": result})
    else:
        return render(request, "contactus.html", {"form": myform})
