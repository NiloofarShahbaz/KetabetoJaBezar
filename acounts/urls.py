from django.urls import path
from . import views
app_name='acounts'

urlpatterns = [
    path('signin/',views.signin, name='signin'),


]
