from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    url('^$', views.index),
    path('', views.index, name="ghar"),
    path('create-user', views.createuser.as_view(), name="signup"),
    path('about-hotel', views.showaboutus, name="aboutus"),
    path('login-user', views.mylogin, name="login"),
    path('rooms', views.AllRooms, name="rooms"),

    # url("^create-profile$", views.createuser),
]