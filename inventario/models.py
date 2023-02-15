from django.db import models
from django.forms import ModelForm
from django.urls import  reverse


# Models
class Book(models.Model):
    id = models.BigAutoField(null=False, unique=True, primary_key=True)
    title = models.CharField(null=False, unique=True, max_length=255)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    publish_date = models.DateField(null=False)
    isbn = models.CharField(null=False, unique=True, max_length=120)

    class Meta:
        ordering=('title',)

    def __str__(self):
        return self.title
    
    def get_url(self):
       return reverse('book_details', args=[self.id])


class Author(models.Model):
    id = models.BigAutoField(null=False, unique=True, primary_key=True)
    name = models.CharField(null=False, unique=True, max_length=255)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    def __str__(self):
        return self.name    
    

class Genre(models.Model):
    id = models.BigAutoField(null=False, unique=True, primary_key=True)
    type = models.CharField(null=False, unique=True, max_length=255)

    def __str__(self):
        return self.type

# ModelForms
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'publish_date', 'isbn']

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'genre']

class GenreForm(ModelForm):
    class Meta:
        model = Genre
        fields = ['type']
