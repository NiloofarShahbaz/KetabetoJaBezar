# Create your models here.

from django.conf import settings
from django.db import models
from django_jalali.db import models as jmodels
from django.utils.crypto import get_random_string
from osm_field.fields import OSMField,LatitudeField,LongitudeField

class Book(models.Model):
    book_name = models.CharField(max_length=300)
    book_author = models.CharField(max_length=300)
    picture=models.URLField()
    ISBN=models.CharField(max_length=17)
    translator=models.CharField(max_length=300,blank=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='User_Book', through_fields=('book', 'user'))
    BID = models.CharField(max_length=5, editable=False)

    def __str__(self):
        return str(self.pk) + ' ' + self.book_name+ self.BID

    def save(self,*args,**kwargs):
        #TODO : check for uniqueness
        self.BID=get_random_string(length=5)
        super().save(*args,**kwargs)

class Location(models.Model):
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()

class User_Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    address = models.OneToOneField(Location,on_delete=models.CASCADE)
    release_date = jmodels.jDateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username + ' ' + self.book.book_name + ' ' + str(self.release_date)



class TempBook(models.Model):
    name=models.CharField(max_length=300)
    author=models.CharField(max_length=300)
    pic=models.URLField(blank=True)
    ISBN=models.CharField(max_length=17)
    translator=models.CharField(max_length=300,blank=True)

