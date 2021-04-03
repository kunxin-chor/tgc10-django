from django import forms
from .models import Book, Publisher, Genre, Tag


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'desc', 'ISBN', 'genre', 'cost',
                  'tags', 'publisher', 'authors', 'owner', 'image')


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ('name', 'email')


class SearchForm(forms.Form):
    # searching by title is optional
    title = forms.CharField(max_length=100, required=False)
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False)
