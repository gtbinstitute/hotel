import datetime

from django import template

from hotel.models import RoomCategory

register = template.Library()


@register.simple_tag
def my_current_time():
    return datetime.datetime.now()


@register.inclusion_tag('fetchrooms.html')
def fetch_rooms():
    queryset = RoomCategory.objects.all().order_by('-roomsavailable')
    context = {"rooms": queryset}
    return context
