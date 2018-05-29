
from django.contrib.auth import get_user_model
# Register your models here.
from django.contrib import admin
from .models import Profile
# Register your models here.
admin.site.register(Profile)
#admin.site.register(get_user_model())
