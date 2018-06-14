from django import forms
from .models import User_Book,Book,TempBook,Location
from django.core.validators import RegexValidator

class TempBookForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['book_name'].widget.attrs['placeholder']=' نام کتاب'
        self.fields['book_name'].widget.attrs['class'] = "add_holder"
        # self.fields['book_author'].widget.attrs['placeholder'] = 'نویسنده کتاب'
        # self.fields['book_author'].widget.attrs['class'] = "add_holder"

    class Meta:
        model=Book
        fields=('book_name',)


class BookForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        persianregex = r'([\u0621-\u0629]*[\u062A-\u063A]*[\u0641-\u0643]*[\u0644-\u064B]*(\u064D)*[\u064E-\u0651]*(\u0655)*(\u067E)*(\u0686)*(\u0698)*[\u06A9-\u06AF]*(\u06D5)*(\u06BE)*(\u06CC)*(\u0020)*[\u2000-\u200F]*[\u2028-\u202F]*[\u06F0-\u06F9]*[\u0660-\u0669]*)+'
        persian_validator=RegexValidator(persianregex,'به فارسی وارد کنید')

        self.fields['name'].widget.attrs['placeholder']=' نام کتاب'
        self.fields['name'].widget.attrs['class'] = "add_holder"
        self.fields['name'].widget.validators=persian_validator

        self.fields['author'].widget.attrs['placeholder'] = 'نویسنده کتاب'
        self.fields['author'].widget.attrs['class'] = "add_holder"
        self.fields['author'].widget.validators = persian_validator

        self.fields['translator'].widget.attrs['placeholder'] = 'مترجم کتاب(در صورت وجود)'
        self.fields['translator'].widget.attrs['class'] = "add_holder"
        self.fields['translator'].widget.validators = persian_validator



        self.fields['ISBN'].widget.attrs['placeholder'] = 'شابک کتاب'
        self.fields['ISBN'].widget.attrs['class'] = "add_holder"

    class Meta:
        model=TempBook
        fields=('name','author','ISBN','translator')


class LocationForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['location'].widget.attrs['placeholder']='آدرس'
        self.fields['location'].widget.attrs['class'] = "add_holder"
        self.fields['location'].required=True

        self.fields['location_lat'].widget.attrs['placeholder'] = 'عرض جغرافیایی'
        self.fields['location_lat'].widget.attrs['class'] = "add_holder"
        self.fields['location_lat'].required = True

        self.fields['location_lon'].widget.attrs['placeholder'] = 'طول جغرافیایی'
        self.fields['location_lon'].widget.attrs['class'] = "add_holder"
        self.fields['location_lon'].required = True

        self.fields['details'].widget.attrs['placeholder'] = 'توضیحات بیشتر'
        self.fields['details'].widget.attrs['class'] = "add_holder"


    class Meta:
        model=Location
        fields=('location','location_lat','location_lon','details')
