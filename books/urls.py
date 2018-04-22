from django.urls import path
from . import views
app_name='books'

urlpatterns = [
    path('',views.BookListView.as_view(), name='booklist'),
    path('new/',views.BookList_NewRealesed.as_view(), name='booklist_newreleased'),
    path('alpha/',views.BookList_Alphabetical.as_view(), name='booklist_alphabetical'),
    path('<uuid:pk>/', view=views.BookDetailView.as_view(), name='bookdetail'),
    path('search/',views.BookSearch.as_view(),name='search'),
    path('search/searchby',views.BookSearchBy.as_view(),name='search_by'),
]
