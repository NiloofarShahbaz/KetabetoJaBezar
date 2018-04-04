# Create your views here.
from django.shortcuts import render
from .models import Book,User_Book
from django.views import generic

class BookListView(generic.ListView):
    template_name = 'pages/books.html'
    context_object_name = 'user_book'
    def get_queryset(self):
        return User_Book.objects.order_by('release_date').reverse()


class BookDetailView(generic.DetailView):
    model = User_Book
    template_name = 'pages/bookdetail.html'
