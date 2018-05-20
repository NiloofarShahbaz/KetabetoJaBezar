from django import forms
from django.contrib.auth import forms as f
from django.contrib.auth import get_user_model
from .models import Profile

class LoginForm(f.AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder']='نام کاربری خود را وارد کنید'
        self.fields['password'].widget.attrs['placeholder']='گذرواژه خود را وارد کنید'

class SingUpForm(f.UserCreationForm):
    email= forms.CharField(max_length=300,required=True,widget=forms.EmailInput(attrs={'placeholder':'پست الکترونیکی خود را وارد کنید'}),)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='نام خود را وارد کنید'
        self.fields['last_name'].widget.attrs['placeholder'] = 'نام خانوادگی خود را وارد کنید'
        self.fields['username'].widget.attrs['placeholder'] = 'نام کاربری برای خود انتخاب کنید'
        self.fields['password1'].widget.attrs['placeholder'] = 'گذرواژه مناسب برای خود انتخاب کنید'
        self.fields['password2'].widget.attrs['placeholder'] = 'گذرواژه انتخابی خود را دوباره وارد کنید'
        self.fields['email'].label='پست الکترونیکی'

    class Meta:
        model=get_user_model()
        fields= ('first_name','last_name','email','username','password1','password2')


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your First Name',
                                                               'class': 'add_holder'}), max_length=30, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Your Last Name',
                                                              'class': 'add_holder'}), max_length=30, required=False)
    bio=forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Bio',
                                                      'class': 'add_holder'}),max_length=500,required=False)

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        try:
            self.fields['first_name'].initial=self.instance.user.first_name
            self.fields['last_name'].initial=self.instance.user.last_name
            self.fields['bio'].initial=self.instance.bio
            self.fields['first_name'].label='نام من'
            self.fields['last_name'].label = 'نام خانوادگی من'
            self.fields['bio'].label='درباره ی من'

        except get_user_model().DoesNotExist:
            pass

    class Meta:
        model=get_user_model()
        fields=('first_name','last_name','bio')

    def save(self, *args,**kwargs):
        u=self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile=super().save(*args,**kwargs)
        return profile

class PassResetForm(f.PasswordResetForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].widget.attrs['placeholder']='پست الکرونیکی خود را وارد کنید '


class PassResetSetForm(f.SetPasswordForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'

class PassChangeForm(f.PasswordChangeForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['old_password'].widget.attrs['placeholder'] = 'Enter Your Old Password'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter Your New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Your New Password'
