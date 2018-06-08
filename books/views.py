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
import googlesearch
from bs4 import BeautifulSoup
import requests


from books.spider import QuotesSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals



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

        book_form = BookForm(request.POST)
        if book_form.is_valid():
            book=book_form.save(commit=False)


            searchfield='کتاب'+' '+book.book_name+' '+'فیدیبو'


            try:
                runner = CrawlerRunner()
                d=runner.crawl(QuotesSpider,search_parameter=searchfield)
                d.addBoth(lambda _: reactor.stop())
                reactor.run()  # the script will block here until the crawling is finished
            except:
                results=googlesearch.search(searchfield,stop=1,num=10)
                file = open('search_results.txt', 'a')
                for item in results:
                    print('google seacch !!!:|')
                    file.write(item)
                    file.write('\n')
                file.close()

            file = open('search_results.txt', 'r')
            f=file.read()
            results=f.split('\n')

            result=results[0]
            result=str(result)
            if result[0:23]=='http://fidibo.com/book/':

                page=requests.get(result)

                soup=BeautifulSoup(page.text,'html.parser')

                infoclass=soup.find(class_='col-sm-10')
                info=infoclass.find_all('a')
                bookname=info[0].contents[0]


                #if bookname==book.book_name:
                bookauthor=info[1].find_all('span')
                bookauthor=bookauthor[0].contents[0]
                book.book_author=bookauthor

                picdiv=soup.find(class_='bov-img')
                pictag=picdiv.find_all('img')[0]
                pic=pictag['src']
                book.picture=pic

                book.save()
            file.close()
            os.remove('search_results.txt')



    else:
        book_form = BookForm()
        book=None
    return render(request,template_name,{'book_form':book_form,'book_name':bookname,'book_author':bookauthor,'book_pic':pic})

def confirm(request,pkk,BID,name):
    template_name='pages/addbookconfirm.html'
    book=Book.objects.get(id=pkk)
    if request.method=='POST':
        user_book_form=User_BookForm(request.POST)
        if user_book_form.is_valid():
            user_book = user_book_form.save(commit=False)
            user_book.book=book
            user_book.user=request.user
            user_book.save()
            return redirect('books:booklist',pkk=book.id)

    else:
        user_book_form=User_BookForm()


    context={'book':book,'user_book_form':user_book_form}
    return render(request,template_name,context)

def download(request,pkk,BID,name):
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
