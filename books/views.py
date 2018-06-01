# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.postgres.search import SearchVector
from .models import Book,User_Book
from django.views.generic import ListView,DetailView,TemplateView
from django.db.models import Max
from .forms import User_BookForm,BookForm
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
import pdfkit
from django.http import HttpResponse
import os
from jdatetime import datetime

class HomePage(TemplateView):
    template_name='homepage.html'


def bookhistory(request):
    template_name = 'bookhistory.html'
    field = request.GET.get('field')
    book=get_object_or_404(Book,BID=field)
    check=User_Book.objects.filter(book=book,address='')
    if not check:
        user_book=User_Book(user=request.user,book=book,address='')
        user_book.save()

    record=User_Book.objects.select_related('book').filter(book__BID=field).order_by('release_date').reverse()
    record=list(record)
    for counter in range(0,len(record)):
        record[counter]=(record[counter],counter%2)

    return render(request,template_name,{'record':record,'book':book})




class BookListView(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'
    paginate_by = 6

    def get_queryset(self):
        list = User_Book.objects.values('book').annotate(Max('release_date'))

        nulls= User_Book.objects.filter(address='').values('id','book')

        include=[]
        date=[]
        for item in list:
            for null in nulls:
                if item['book']==null['book']:
                    break
            else:
                include.append(item['book'])
                date.append(item['release_date__max'])


        return User_Book.objects.filter(book__in=include,release_date__in=date).order_by('release_date').reverse()


class BookList_Alphabetical(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'
    paginate_by = 6

    def get_queryset(self):
        list = User_Book.objects.values('book').annotate(Max('release_date'))

        nulls = User_Book.objects.filter(address='').values('id', 'book')

        include = []
        date = []
        for item in list:
            for null in nulls:
                if item['book'] == null['book']:
                    break
            else:
                include.append(item['book'])
                date.append(item['release_date__max'])

        return User_Book.objects.filter(book__in=include, release_date__in=date).order_by('book__book_name')


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
            list = User_Book.objects.values('book').annotate(Max('release_date'))

            nulls = User_Book.objects.filter(address='').values('id', 'book')

            include = []
            date = []
            for item in list:
                for null in nulls:
                    if item['book'] == null['book']:
                        break
                else:
                    include.append(item['book'])
                    date.append(item['release_date__max'])

            return User_Book.objects.filter(book__in=include, release_date__in=date).order_by('release_date') \
                .annotate(search=SearchVector('book__book_name', 'book__book_author', 'address')) \
                .filter(search=field).reverse()
        else:
            return None

@login_required
def addbook(request):
    template_name = 'pages/AddBookPage.html'

    if request.method=='POST':
        user_book_form = User_BookForm(request.POST)
        book_form = BookForm(request.POST)
        if user_book_form.is_valid() and book_form.is_valid():
            book=book_form.save()
            user_book=user_book_form.save(commit=False)
            user_book.book=book
            user_book.user=request.user
            user_book.save()
            return redirect('books:confirm',pkk=book.id)

    else:
        user_book_form = User_BookForm()
        book_form = BookForm()
    return render(request,template_name,{'user_book_form':user_book_form,'book_form':book_form})

def confirm(request,pkk):
    template_name='pages/addbookconfirm.html'
    book=Book.objects.get(id=pkk)
    context={'pkk':book.pk}
    return render(request,template_name,context)

def download(request,pkk):
    book = Book.objects.get(id=pkk)
    context = {'BID': book.BID,'name':book.book_name,'author':book.book_author}
    template = get_template('pdffile.html')
    html = template.render(context)
    pdfkit.from_string(html, 'book.pdf')
    with open('book.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')  # Generates the response as pdf response.
        response['Content-Disposition'] = 'attachment; filename=Book.pdf'
        pdf.close()
    os.remove("book.pdf")  # remove the locally created pdf file.
    return response


def leavebook(request):
    template_name='pages/leavebook.html'
    if request.method=='POST':

        bid=request.POST.get('bid')
        address=request.POST.get('address')

        book=get_object_or_404(Book,BID=bid)
        user_book=get_object_or_404(User_Book,book=book,user=request.user,address='')

        user_book.address=address
        user_book.release_date=datetime.now()
        user_book.save()


        return redirect('books:booklist')


    return render(request,template_name)
