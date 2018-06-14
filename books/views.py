# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.postgres.search import SearchVector
from .models import Book,User_Book,TempBook,Location
from django.views.generic import ListView,DetailView,TemplateView
from django.db.models import Max
from .forms import BookForm,TempBookForm,LocationForm
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

    check = User_Book.objects.filter(book=book, address=None)
    print(check)
    if not check:
        user_book = User_Book(user=request.user, book=book, address=None,release_date=datetime.now())
        user_book.save()

    record=User_Book.objects.select_related('book').filter(book__BID=field).order_by('release_date').reverse()
    record=list(record)
    for counter in range(0,len(record)):
        location = []
        if record[counter].address:
            location = record[counter].address.location
            location = location.split(',')
        newloc=''
        for l in location:
            if l==' Tehran':
                newloc = newloc + l
                break
            newloc = newloc + l + ','
        record[counter]=(record[counter],counter%2,newloc)

    return render(request,template_name,{'record':record,'book':book})


def addlocation(request,pk):
    template_name='pages/addlocation.html'
    book=Book.objects.get(pk=pk)
    if request.method=='POST':
        form=LocationForm(request.POST)
        location=form.save()
        location.save()
        return redirect('books:confirmlocation',pk,location.pk)

    else:
        form=LocationForm()
    return render(request,template_name,{'form':form,'book':book})


def confirmlocation(request,pk,loc):
    template_name='pages/confirmlocation.html'
    book=Book.objects.get(pk=pk)
    location=Location.objects.get(pk=loc)
    custom_loc=location.location.split(',')
    newloc=''
    for l in custom_loc:
        if l == ' Tehran':
            newloc = newloc + l
            break
        newloc = newloc + l + ','

    if request.method=='POST':
        user=request.user
        user_book=User_Book(user=user,book=book,address=location,release_date=datetime.now())
        user_book.save()
        return redirect('books:booklist')
    return render(request,template_name,{'book':book,'location':location,'loc':newloc})



class BookListView(ListView):
    template_name = 'pages/BookListPage.html'
    context_object_name = 'user_book'
    paginate_by = 6

    def get_queryset(self):
        list = User_Book.objects.values('book').annotate(Max('release_date'))

        nulls= User_Book.objects.filter(address=None).values('id','book')

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

        nulls = User_Book.objects.filter(address=None).values('id', 'book')

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

            nulls = User_Book.objects.filter(address=None).values('id', 'book')

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
                .annotate(search=SearchVector('book__book_name', 'book__book_author', 'address__location')) \
                .filter(search=field).reverse()
        else:
            return None

@login_required
def addbook(request):
    template_name = 'pages/AddBookPage.html'

    if request.method=='POST':

        book_form = TempBookForm(request.POST)
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
                    file.write(item)
                    file.write('\n')
                file.close()

            file = open('search_results.txt', 'r')
            f=file.read()
            results=f.split('\n')

            books=[]
            for i in range(0,5):
                tempbook = TempBook()
                result=results[i]
                result=str(result)
                print(result)
                if result[0:23]=='http://fidibo.com/book/':
                    page=requests.get(result)

                    soup=BeautifulSoup(page.text,'html.parser')

                    infoclass=soup.find(class_='col-sm-10')
                    info=infoclass.find_all('a')
                    tempbook.name=info[0].contents[0]
                    if tempbook.name[-9:]=='نسخه صوتی':
                        break

                    author=info[1].find_all('span')
                    tempbook.author=author[0].contents[0]

                    if len(info)==3:
                        translator=info[2].find_all('span')
                        tempbook.translator=translator[0].contents[0]

                    isbndiv=soup.find(class_='book-tags')
                    isbntag=isbndiv.find_all('label')
                    print(isbntag[0].prettify())
                    for isbn in isbntag[0].contents:
                        tempbook.ISBN=isbn[::-1]





                    picdiv=soup.find(class_='bov-img')
                    pictag=picdiv.find_all('img')[0]
                    tempbook.pic=pictag['src']

                    tempbook.save()

                    books.append(tempbook)


            file.close()
            os.remove('search_results.txt')



    else:
        book_form = TempBookForm()
        books=None
    return render(request,template_name,{'book_form':book_form,'books':books})



def addbookmanualy(request):
    template_name='pages/addbookmanualy.html'
    if request.method=='POST':
        book_form=BookForm(request.POST)
        if book_form.is_valid():
            tempbook=book_form.save()
            tempbook.save()
            return redirect('books:confirmbook',pk=tempbook.pk)
    else:
        book_form=BookForm()
    return render(request,template_name,{'book_form':book_form})


def confirmbook(request,pk):
    template_name='pages/addbookconfirm.html'

    tmpbook = TempBook.objects.get(pk=pk)
    return render(request,template_name,{'book':tmpbook})





def downloadpdf(request,pk):
    template_name = 'pages/downloadpdf.html'

    tmpbook = TempBook.objects.get(pk=pk)
    book = Book(book_name=tmpbook.name, book_author=tmpbook.author, picture=tmpbook.pic, ISBN=tmpbook.ISBN,
                translator=tmpbook.translator)
    book.save()
    TempBook.objects.all().delete()

    return render(request,template_name,{'pk':book.pk})

def download(request,pk):
    book = Book.objects.get(id=pk)
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
        form=LocationForm(request.POST)
        location=form.save()
        location.save()

        book=get_object_or_404(Book,BID=bid)

        return redirect('books:leavebookconfirm',pk=book.pk,loc=location.pk)
    else:
        form=LocationForm()

    return render(request,template_name,{'form':form})

def leavebookconfirm(request,pk,loc):
    template_name = 'pages/leavebookconfirm.html'
    book = get_object_or_404(Book, pk=pk)
    location = get_object_or_404(Location, pk=loc)
    custom_loc = location.location.split(',')
    newloc = ''
    for l in custom_loc:
        if l == ' Tehran':
            newloc = newloc + l
            break
        newloc = newloc + l + ','
    time=datetime.now()
    if request.method=='POST':
        user_book=get_object_or_404(User_Book,book=book,user=request.user,address=None)
        user_book.address=location
        user_book.release_date=datetime.now()
        user_book.save()
        return redirect('books:booklist')
    return render(request,template_name,{'book':book,'location':location,'time':time,'loc':newloc})
