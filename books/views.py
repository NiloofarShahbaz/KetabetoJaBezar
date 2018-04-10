# Create your views here.
from django.shortcuts import render
from .models import Book,User_Book
from django.views.generic import ListView,DetailView



class BookListView(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'
    def get_queryset(self):
        return User_Book.objects.order_by('release_date').reverse()

class BookList_Alphabetical(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'

    def get_queryset(self):
        return User_Book.objects.order_by('book__book_name')

class BookList_NewRealesed(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'

    def get_queryset(self):
        return User_Book.objects.order_by('release_date').reverse()

class BookDetailView(DetailView):
    model = User_Book
    template_name = 'pages/BookDetails.html'
