# coding: utf-8

#         app: org.toledano.blogApp
#      module: blog.views
# description: Views for blog app
#      author: Javier Sanchez Toledano
#        date: 2022-08-20
#     licence: MIT
#      python: 3.10

from django.views.generic import ListView, DetailView

from . import models


class IndexView(ListView):
    template_name = 'blog/index.html'
    queryset = models.Entry.objects.all().order_by('-pub_date')[:4]
    context_object_name = 'entries'


class BlogIndex(ListView):
    template_name = 'blog/blogIndex.html'
    context_object_name = 'entries'
    model = models.Entry
    paginate_by = 6


class CategoryList(ListView):
    model = models.Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 6


class CategoryDetail(DetailView):
    model = models.Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'category'
    paginate_by = 6
    allow_empty = True
    slug_field = 'slug'


class EntryDetail(DetailView):
    model = models.Entry
    context_object_name = 'entry'
