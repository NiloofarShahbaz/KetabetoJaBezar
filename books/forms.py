from django import forms
from .models import User_Book,Book


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
        self.fields['book_name'].widget.attrs['placeholder']=' نام کتاب'
        self.fields['book_name'].widget.attrs['class'] = "add_holder"
        # self.fields['book_author'].widget.attrs['placeholder'] = 'نویسنده کتاب'
        # self.fields['book_author'].widget.attrs['class'] = "add_holder"

    class Meta:
        model=Book
        fields=('book_name',)


class User_BookForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['address'].widget.attrs['placeholder']='آدرس'
        self.fields['address'].widget.attrs['class'] = "add_holder"
        self.fields['address'].required=True

    class Meta:
        model=User_Book
        fields=('address',)



