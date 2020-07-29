from django.conf.urls import url
from django.urls import path

from gtbdjango.hotel import views

urlpatterns = [
    url('^$', views.index),
    path('', views.index, name="home"),
    path('create-user', views.createuser, name="signup"),
    path('about-hotel', views.showaboutus, name="aboutus"),
    # url("^create-profile$", views.createuser),
]