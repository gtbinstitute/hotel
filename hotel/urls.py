from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from gtb import settings
from . import views

urlpatterns = [
    url('^$', views.index),
    path('', views.index, name="ghar"),
    path('create-user', views.createuser.as_view(), name="signup"),
    path('about-hotel', views.showaboutus, name="aboutus"),
    path('login-user', views.mylogin, name="userlogin"),
    path('rooms', views.AllRooms, name="rooms"),
    path('room-details/<int:catid>', views.RoomDetails, name="myroomdetails"),
    path('signout', views.mysignout, name='signout'),
    path('user-profile', views.useraccount, name='myaccount'),
    path('update-profile', views.updateuser, name='updateprofile'),
    path('change-password', views.changepassword, name='changepassword'),
    path('room-booking/<int:detailid>', views.booking, name='booking'),
    path('contact-us', views.showcontactus, name="contactus"),
    # url("^create-profile$", views.createuser),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

