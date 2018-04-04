 #Create your models here.
from uuid import uuid4
from django.conf import settings
from django.db import models
 # Create your models here.
class Book(models.Model):
    book_name=models.CharField(max_length=300)
    book_author=models.CharField(max_length=300)
    user=models.ManyToManyField(settings.AUTH_USER_MODEL,through='User_Book',through_fields=('book','user'))
    def __str__(self):
        return str(self.pk)+ ' '+self.book_name

class User_Book(models.Model):
    BID = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE)
    address = models.CharField(max_length=2000)
    release_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username +' '+self.book.book_name+' '+str(self.release_date)
