import random

from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class RoomCategory(models.Model):
    categoryname = models.CharField(max_length=30)
    features = RichTextField()
    roomsavailable = models.IntegerField(default=0)
    Image = models.ImageField(upload_to='pics', blank='True', null='True')

    def __str__(self):
        return self.categoryname


class RoomCategoryDetails(models.Model):
    roomcategoryid = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    roomoptions = models.CharField(max_length=200)
    roomprice = models.IntegerField()

    def __str__(self):
        return str(self.roomcategoryid)


class Booking(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    roomcategoryid = models.ForeignKey(RoomCategory, on_delete=models.CASCADE)
    roomdetailid = models.ForeignKey(RoomCategoryDetails, on_delete=models.CASCADE)
    checkindate = models.DateField()
    checkoutdate = models.DateField()
    amount = models.IntegerField()
    totalpersons = models.IntegerField()
    guestname = models.CharField(max_length=70)
    gender_choices = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=6, choices=gender_choices)


def random_string():
    return str(random.randint(10000, 99999))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
