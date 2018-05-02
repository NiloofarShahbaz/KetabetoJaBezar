from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
from . import views
app_name='acounts'

urlpatterns = [
    path('signin/',LoginView.as_view(template_name='account/SignPage.html'), name='signin'),
    path('signup/',views.SignUpView.as_view(), name='signup'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('<username>/',views.profileview,name='profile'),
    path('settings/edit/',views.editprofile,name='settings'),
    path('settings/edit/',views.editprofile,name='edit'),

]
