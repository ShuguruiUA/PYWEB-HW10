from django.urls import path
from . import views


app_name = "quotesapp"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page>", views.index, name="index_paginate"),
    path("add_tag/", views.add_tag, name="add_tag"),
    path("add_author/", views.add_author, name="add_author"),
    path("add_quote/", views.add_quote, name="add_quote"),
    path("author/<int:author_id>", views.author_info, name="author"),
    path("tag/<str:tag_name>/<int:page>/", views.tag_info, name='tag_info')
]
