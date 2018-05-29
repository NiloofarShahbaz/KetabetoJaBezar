from django import forms
from .models import User_Book,Book


class BookForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['book_name'].widget.attrs['placeholder']=' نام کتاب'
        self.fields['book_name'].widget.attrs['class'] = "add_holder"
        self.fields['book_author'].widget.attrs['placeholder'] = 'نویسنده کتاب'
        self.fields['book_author'].widget.attrs['class'] = "add_holder"

    class Meta:
        model=Book
        fields=('book_name','book_author')


class User_BookForm(forms.ModelForm):
    # book_author = forms.CharField(widget=forms.TextInput(attrs={'class': "add_holder", 'placeholder': 'نویسنده کتاب'}),
    #                             max_length=200, required=True)
    # book_name=forms.CharField(widget=forms.TextInput(attrs={'class':"add_holder",'placeholder': 'نام کتاب'}),
    #                           max_length=200, required=True)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['address'].widget.attrs['placeholder']='آدرس'
        self.fields['address'].widget.attrs['class'] = "add_holder"
        self.fields['address'].required=True

    class Meta:
        model=User_Book
        fields=('address',)

