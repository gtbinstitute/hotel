from django.conf.urls import url

from gtbdjango.hotel import views

urlpatterns = [
    url('^$', views.index)
]