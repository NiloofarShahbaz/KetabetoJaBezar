from django.urls import path
from . import views
app_name='books'

urlpatterns = [
    path('',views.BookListView.as_view(), name='booklist'),
    path('new/',views.BookListView.as_view(), name='booklist_newreleased'),
    path('alpha/',views.BookList_Alphabetical.as_view(), name='booklist_alphabetical'),
    path('<int:pk>/', view=views.BookDetailView.as_view(), name='bookdetail'),
    path('search/',views.BookSearch.as_view(),name='search'),
    path('search/searchby',views.BookSearchBy.as_view(),name='search_by'),
    path('addbook/',views.addbook,name='addbook'),
    path('addbook/<isbn>/',views.downloadpdf,name='downloadpdf'),
    path('addbook/<pkk>/download',views.download,name='dl'),
    path('leavebook/',views.leavebook,name='leavebook'),
]
