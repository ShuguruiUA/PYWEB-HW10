from django.forms import ModelForm, CharField, TextInput, DateInput, Textarea, ModelChoiceField, Select, SelectMultiple, \
    MultipleChoiceField
from .models import Author, Tag, Quote


class AuthorForm(ModelForm):
    fullname = CharField(min_length=3, max_length=20, required=True, widget=TextInput())
    born_date = CharField(max_length=50, widget=TextInput())
    born_location = CharField(max_length=50, widget=TextInput())
    description = CharField(max_length=255, widget=TextInput())

    class Meta:
        model = Author
        fields = ('fullname', 'born_date', 'born_location', 'description')


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=50, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ('name',)


class QuoteForm(ModelForm):
    quote = CharField(widget=Textarea(attrs={"class": "form-control", "rows": 5}))
    author = ModelChoiceField(queryset=Author.objects.all(), widget=Select(attrs={"class": "form-control"}))
    tags = MultipleChoiceField(
        widget=SelectMultiple(attrs={"class": "form-control", "rows": 5}),
        choices=((tag.id, tag.name) for tag in Tag.objects.all())
    )

    class Meta:
        model = Quote
        fields = ('quote', 'author', 'tags')
