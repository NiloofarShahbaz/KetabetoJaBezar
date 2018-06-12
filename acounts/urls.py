from django.contrib.auth import views as v
from django.urls import path
from . import views,forms
from django.urls import reverse_lazy

app_name='acounts'

urlpatterns = [

    path('signin/',v.LoginView.as_view(template_name='account/SignPage.html',
                                       authentication_form=forms.LoginForm),
                                        name='signin'),
    path('signup/',views.SignUpView.as_view(), name='signup'),

    path('logout/',v.LogoutView.as_view(),name='logout'),


path('settings/',views.editprofile,name='settings'),

    path('settings/edit/',views.editprofile,name='edit'),

    path('settings/password/',v.PasswordChangeView.as_view(
        template_name='account/password_change.html',
        form_class=forms.PassChangeForm,
        success_url = reverse_lazy('acounts:pass_change_done')),
        name='pass_change'),

    path('settings/password/done',v.PasswordChangeDoneView.as_view(
        template_name='account/password_change_done.html'
    ),name='pass_change_done'),

    path('password_reset/',v.PasswordResetView.as_view(
        template_name='account/password_reset.html',
        email_template_name='account/password_reset_email.html',
        subject_template_name='account/password_reset_subject.txt',
        form_class=forms.PassResetForm,
        success_url=reverse_lazy('acounts:pass_reset_done')),
         name='pass_reset'),

    path('password_reset/done/',v.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'),
         name='pass_reset_done'),

    path('reset/<uidb64>/<token>/',v.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confrmation.html',
        form_class=forms.PassResetSetForm,
        success_url = reverse_lazy('acounts:pass_reset_complete')),
         name='pass_reset_confirm'),

    path('reset/done/',v.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'
    ),name='pass_reset_complete'),


    path('<username>/',views.profileview,name='profile'),



]
