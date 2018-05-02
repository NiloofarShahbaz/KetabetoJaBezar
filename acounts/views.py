from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth import get_user_model
from django.views.generic import View,DetailView,UpdateView,ListView
from .forms import SingUpForm,EditProfileForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from books.models import User_Book
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
# Create your views here.
class SignUpView(View):
    form_class=SingUpForm
    template_name='account/SignUpPage.html'

    def get(self,request):
        form=self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form=self.form_class(request.POST)

        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')

        return render(request, self.template_name, {'form': form})



def profileview(request,username):
    requested_user=get_object_or_404(get_user_model(),username__iexact=username)
    template_name='account/profile.html'
    return render(request,template_name,{'thisuser':requested_user})

@login_required
def settings(request):
    print("hi!!!!!!!")
    return redirect('/settings/edit/')

@login_required
def editprofile(request):
    if request.method=='POST':
        form= EditProfileForm(request.POST,instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, u'Your profile were successfully edited.')
            return redirect('acounts:profile',username=request.user.username)
    else:

        form = EditProfileForm(instance=request.user.profile)
    return render(request,'account/profile_edit.html',{'form':form})

# class ProfileView(ListView):
#     template_name = 'account/user.html'
#     context_object_name = 'thisuser'
#     slug_field='username'
#     def get_queryset(self):
#         #return User_Book.objects.select_related('user').filter(user__username=self.kwargs['slug'])
#         return get_user_model().objects.get(username=self.kwargs['slug'])
