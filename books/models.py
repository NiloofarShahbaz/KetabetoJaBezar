# Create your models here.

from django.conf import settings
from django.db import models
from django_jalali.db import models as jmodels
from django.utils.crypto import get_random_string

class Book(models.Model):
    book_name = models.CharField(max_length=300)
    book_author = models.CharField(max_length=300)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, through='User_Book', through_fields=('book', 'user'))
    BID = models.CharField(max_length=5, editable=False)

    def __str__(self):
        return str(self.pk) + ' ' + self.book_name

    def save(self,*args,**kwargs):
        #TODO : check for uniqueness
        self.BID=get_random_string(length=5)
        super().save(*args,**kwargs)

class User_Book(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    address = models.CharField(max_length=2000,blank=True)
    release_date = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.book.book_name + ' ' + str(self.release_date)


