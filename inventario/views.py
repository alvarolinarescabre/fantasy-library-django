from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.http import JsonResponse    
from django.contrib import messages
from django.db.models import Q
from .forms import RegisterForm
from . import models
from . import forms


class BooksListView(LoginRequiredMixin, ListView):
    paginate_by = 2
    model = models.Book

class AuthorsListView(LoginRequiredMixin, ListView):
    paginate_by = 2
    model = models.Author

class GenresListView(LoginRequiredMixin, ListView):
    paginate_by = 2
    model = models.Genre

class SearchResultsView(LoginRequiredMixin, ListView):
    model = models.Book
    template_name = 'inventario/search.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = models.Book.objects.filter(
            Q(title__icontains=query) | Q(author__name__icontains=query) | Q(genre__type__icontains=query)
        )
        return object_list

def books_api(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 2)
    startswith = request.GET.get("startswith", "")
    keywords = models.Book.objects.filter(
        title__startswith=startswith
    )
    paginator = Paginator(keywords, per_page)
    page_obj = paginator.get_page(page_number)
    data = [{"title": book.title} for book in page_obj.object_list]

    payload = {
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "data": data
    }
    return JsonResponse(payload)

def home(request):
    return render(request, 'home/index.html')

def register_request(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful." )
            return redirect("login")
            
        messages.error(request, "Unsuccessful registration. Invalid information.")
        
    form = RegisterForm()    
    
    return render (request=request, template_name="registration/register.html", context={"register_form": form})

def login_request(request):
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.INFO, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.add_message(request, messages.ERROR,"Invalid username or password.")
        else:
            messages.add_message(request, messages.ERROR,"Invalid username or password.")
            
    return render(request=request, template_name="registration/login.html", context={"login_form":form})

@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")

@login_required
def book_detail(request, id, page):
    book = models.Book.objects.filter(id = id)
    return render(request, 'inventario/book_detail.html', {'book': book, 'page': page})

@login_required
def book_add(request):
    form = forms.Book()

    if request.method=="POST":
        form = forms.Book(request.POST)

        # To select the author & genre from Form
        author = models.Author.objects.get(id=request.POST['author'])
        genre = models.Genre.objects.get(id=request.POST['genre'])

        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            genre = form.cleaned_data['genre']
            publish_date = form.cleaned_data['publish_date']
            isbn = form.cleaned_data['isbn']

            # Save Data from Form
            obj=models.Book.objects.create(title=title, author=author, genre=genre, publish_date=publish_date, isbn=isbn)
            obj.save()
        
            return redirect('books', page=1)

    return render(request, 'inventario/book_add.html', {'form':form})

@login_required
def book_modify(request, id):
    book = models.Book.objects.get(id=id)
    form = models.BookForm(instance=book)

    if request.method=="POST":
        form = forms.Book(request.POST)

        # To select the author & genre from Form
        author = models.Author.objects.get(id=request.POST['author'])
        genre = models.Genre.objects.get(id=request.POST['genre'])

        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            genre = form.cleaned_data['genre']
            publish_date = form.cleaned_data['publish_date']
            isbn = form.cleaned_data['isbn']

            # Save Data from Form
            obj = models.Book.objects.filter(pk=id).update(title=title, author=author, genre=genre, publish_date=publish_date, isbn=isbn)

            return redirect('books', page=1)
        
    return render(request, 'inventario/book_modify.html', {'form':form})

@login_required
def book_delete(request, id):
    book = models.Book.objects.get(id=id)
    obj = models.Book.objects.filter(pk=id).delete()

    return redirect('books', page=1)

@login_required
def genre_add(request):
    form = forms.Genre()

    if request.method=="POST":
        form = forms.Genre(request.POST)

        if form.is_valid():
            type = form.cleaned_data['type']

            # Save Data from Form
            obj=models.Genre.objects.create(type=type)
            obj.save()
        
            return redirect('genres', page=1)
        
    return render(request, 'inventario/genre_add.html', {'form':form})

@login_required
def genre_detail(request, id, page):
    genre = models.Genre.objects.filter(id = id)
    return render(request, 'inventario/genre_detail.html', {'genre': genre, 'page': page})

@login_required
def genre_modify(request, id):
    genre = models.Genre.objects.get(id=id)
    form = models.GenreForm(instance=genre)

    if request.method=="POST":
        form = forms.Genre(request.POST)

        if form.is_valid():
            type = form.cleaned_data['type']

            # Save Data from Form
            obj = models.Genre.objects.filter(pk=id).update(type=type)

            return redirect('genres', page=1)
        
    return render(request, 'inventario/genre_modacify.html', {'form':form})

@login_required
def genre_delete(request, id):
    genre = models.Genre.objects.get(id=id)
    obj = models.Genre.objects.filter(pk=id).delete()

    return redirect('genres', page=1)

@login_required
def author_add(request):
    form = forms.Author()

    if request.method=="POST":
        form = forms.Author(request.POST)

        # To select the genre from Form
        genre = models.Genre.objects.get(id=request.POST['genre'])

        if form.is_valid():
            name = form.cleaned_data['name']
            genre = form.cleaned_data['genre']

            # Save Data from Form
            obj=models.Author.objects.create(name=name, genre=genre)
            obj.save()
        
            return redirect('authors', page=1)
    
    return render(request, 'inventario/author_add.html', {'form':form})

@login_required
def author_detail(request, id, page):
    author = models.Author.objects.filter(id = id)
    return render(request, 'inventario/author_detail.html', {'author': author, 'page': page})

@login_required
def author_modify(request, id):
    author = models.Author.objects.get(id=id)
    form = models.AuthorForm(instance=author)

    if request.method=="POST":
        form = forms.Author(request.POST)

        # To select the author & genre from Form
        genre = models.Genre.objects.get(id=request.POST['genre'])

        if form.is_valid():
            name = form.cleaned_data['name']
            genre = form.cleaned_data['genre']

            # Save Data from Form
            obj = models.Author.objects.filter(pk=id).update(name=name, genre=genre)

            return redirect('authors', page=1)
        
    return render(request, 'inventario/author_modify.html', {'form':form})

@login_required
def author_delete(request, id):
    author = models.Author.objects.get(id=id)
    obj = models.Author.objects.filter(pk=id).delete()

    return redirect('authors', page=1)
