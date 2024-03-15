from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AuthorForm, TagForm, QuoteForm
from .models import Quote, Author, Tag
import django

from .utils import get_mongodb


def index(request, page=1):
    # db = get_mongodb()
    # quotes = db.quotes.find()
    quotes = Quote.objects.all().order_by('created_at')

    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, "index.html", context={'quotes': quotes_on_page})


def author_info(request, author_id):
    a = get_object_or_404(Author, id=author_id)
    return render(request, 'author_info.html', context={"Title": "Author details", "author": a})


def tag_info(request, tag_name, page=1):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.all().filter(tags=tag)
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'tag_info.html', context={"quotes": quotes_on_page, "tag": tag, "page": 1})


@login_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST, request.FILES, instance=Tag())
        if form.is_valid():
            form.save()
            messages.success(request, f"Tag '{form.cleaned_data['name']}' has been added!")
            return redirect(to="quotesapp:add_tag")
        return render(request, "add_tag.html", {"form": form})
    return render(request, "add_tag.html", {"form": TagForm()})


@login_required
def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(to="quotesapp:index")
        else:
            return render(request, 'tag.html', {'form': form})
    return render(request, 'tag.html', {'form': TagForm()})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f"Author '{form.cleaned_data['fullname']}' has been added!")
            return redirect(to='quotesapp:add_author')
        else:
            return render(request, 'add_author.html', context={"form": form})
    return render(request, "add_author.html", context={"form": AuthorForm()})


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            quote = form.save()
            selected_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in selected_tags.iterator():
                quote.tag.add(tag)
            quote.save()
            messages.success(request, f"Quote has been added!")
            return redirect(to='quotesapp:add_quote')
        else:
            return render(request, "add_quote.html", context={"form": form})
    return render(request, "add_quote.html", context={"form": QuoteForm()})
