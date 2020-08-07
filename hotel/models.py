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