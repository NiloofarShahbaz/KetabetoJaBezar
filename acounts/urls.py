from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
app_name='acounts'

urlpatterns = [
    path('signin/',LoginView.as_view(template_name='account/SignPage.html'), name='signin'),
    path('signup/',views.SignUpView.as_view(), name='signup'),


]
