from django.urls import path
from . import views
app_name='books'

urlpatterns = [
    path('',views.BookListView.as_view(), name='booklist'),
    path('new/',views.BookListView.as_view(), name='booklist_newreleased'),
    path('alpha/',views.BookList_Alphabetical.as_view(), name='booklist_alphabetical'),
    path('<int:pk>/', view=views.BookDetailView.as_view(), name='bookdetail'),
    path('search/',views.BookSearch.as_view(),name='search'),
    path('search/searchby/',views.BookSearchBy.as_view(),name='search_by'),
    path('addbook/',views.addbook,name='addbook'),
    path('addbook/manualy/',views.addbookmanualy,name='addbookmanualy'),
    path('addbook/confirmbook/<pk>/done/download/',views.download,name='dl'),
    path('addbook/confirmbook/<pk>/done/',views.downloadpdf,name='downloadpdf'),
    path('addbook/confirmbook/<pk>/',views.confirmbook,name='confirmbook'),
    path('addbook/<pk>/addlocation/<loc>/',views.confirmlocation,name='confirmlocation'),
    path('addbook/<pk>/addlocation/',views.addlocation,name='addlocation'),
    path('leavebook/',views.leavebook,name='leavebook'),
]
