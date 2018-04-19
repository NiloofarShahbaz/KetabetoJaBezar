from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.views.generic import View
from .forms import SingUpForm

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


            login(request,user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        return render(request, self.template_name, {'form': form})


def signin(request):
    return render(request,'account/SignPage.html')
