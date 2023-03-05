from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("registration/register", views.register_request, name="register"),
    path("registration/login", views.login_request, name="login"),
    path("registration/logout", views.logout_request, name= "logout"),
    path('accounts/login/', views.login_request, name="accounts_login"),
    path('accounts/logout/', views.logout_request, name="accounts_logout"),
    path('inventario/books/<int:page>', views.BooksListView.as_view(), name='books'),
    path('inventario/book_details/<int:id>/<int:page>', views.book_detail, name='book_details'),
    path('inventario/book_add', views.book_add, name='book_add'),
    path('inventario/book_modify/<int:id>', views.book_modify, name='book_modify'),
    path('inventario/book_delete/<int:id>', views.book_delete, name='book_delete'),
    path('inventario/genres/<int:page>', views.GenresListView.as_view(), name='genres'),
    path('inventario/genre_details/<int:id>/<int:page>', views.genre_detail, name='genre_details'),
    path('inventario/genre_add', views.genre_add, name='genre_add'),
    path('inventario/genre_modify/<int:id>', views.genre_modify, name='genre_modify'),
    path('inventario/genre_delete/<int:id>', views.genre_delete, name='genre_delete'),
    path('inventario/authors/<int:page>', views.AuthorsListView.as_view(), name='authors'),
    path('inventario/author_details/<int:id>/<int:page>', views.author_detail, name='author_details'),
    path('inventario/author_add', views.author_add, name='author_add'),
    path('inventario/author_modify/<int:id>', views.author_modify, name='author_modify'),
    path('inventario/author_delete/<int:id>', views.author_delete, name='author_delete'),
    path('inventario/search/', views.SearchResultsView.as_view(), name="search"),
    path("books.json", views.books_pagination, name="books_pagination"),
]