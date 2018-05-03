# Create your views here.
from django.shortcuts import render
from django.contrib.postgres.search import SearchVector
from .models import Book,User_Book
from django.views.generic import ListView,DetailView,TemplateView



class BookListView(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'
    paginate_by = 15
    def get_queryset(self):
        return User_Book.objects.select_related('book').order_by('release_date').reverse()

class BookList_Alphabetical(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'
    paginate_by = 15
    def get_queryset(self):
        return User_Book.objects.select_related('book').order_by('book__book_name')

class BookList_NewRealesed(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'
    paginate_by = 15
    def get_queryset(self):
        return User_Book.objects.select_related('book').order_by('release_date').reverse()

class BookDetailView(DetailView):
    model = User_Book
    template_name = 'pages/BookDetails.html'

class BookSearch(TemplateView):
    template_name='pages/SearchPage.html'

class BookSearchBy(ListView):
    template_name = 'pages/SearchPage.html'
    context_object_name = 'result'

    def get_queryset(self):
        field=self.request.GET.get('field')
        if field:
            return User_Book.objects.select_related('book').order_by('book')\
                .annotate(search=SearchVector('book__book_name','book__book_author','address'))\
                .filter(search=field)

class BookAdd(TemplateView):
    template_name = 'pages/AddBookPage.html'
