from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

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


