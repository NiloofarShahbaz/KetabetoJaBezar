from django.contrib import admin
from .models import Book,User_Book,TempBook
# Register your models here.
admin.site.register(Book)
admin.site.register(User_Book)
admin.site.register(TempBook)
