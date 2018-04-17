from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class SingUpForm(UserCreationForm):
    email= forms.CharField(max_length=300,required=True,widget=forms.EmailInput(attrs={'placeholder':'Email'}),)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['username'].widget.attrs['placeholder'] = 'Choose A UserName'
        self.fields['password1'].widget.attrs['placeholder'] = 'Choose A Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat Password'

    class Meta:
        model=get_user_model()
        fields= ('first_name','last_name','email','username','password1','password2')
