from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


class RegisterForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
	
class Book(forms.Form):
    title = forms.CharField(max_length=255)
    author = forms.ModelChoiceField(queryset=models.Author.objects.only())
    genre = forms.ModelChoiceField(queryset=models.Genre.objects.all())
    publish_date = forms.DateField()
    isbn = forms.CharField(max_length=120)

class Author(forms.Form):
    name = forms.CharField(max_length=255)
    genre = forms.ModelChoiceField(queryset=models.Genre.objects.all())

class Genre(forms.Form):
    type = forms.CharField(max_length=255)
