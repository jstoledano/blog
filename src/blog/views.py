# coding: utf-8
#         app: org.toledano.blogApp
#      module: blog.views
# description: Views for blog app
#      author: Javier Sanchez Toledano
#        date: 2022-08-20
#     licence: MIT
#      python: 3.10

from django.shortcuts import render
from django.views.generic import ListView, DetailView

from . import models


class IndexView(ListView):
    template_name = 'blog/index.html'
    queryset = models.Entry.objects.all().order_by('-pub_date')[:4]
    context_object_name = 'entries'


class BlogIndex(ListView):
    queryset = models.Entry.objects.exclude(featured=True)[4:]
    template_name = 'index.html'
    context_object_name = 'entries'
    model = models.Entry
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sticky'] = models.Entry.objects.filter(featured=True)[0]
        context['primeros'] = models.Entry.objects.all()[:4]
        context['featured'] = models.Entry.objects.filter(featured=True)[1:6]
        return context


class CategoryList(ListView):
    model = models.Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10


class CategoryDetail(DetailView):
    model = models.Category
    template_name = 'blog/category_detail.html'
    context_object_name = 'entries'
    paginate_by = 6
    allow_empty = True
    slug_field = 'slug'


class EntryDetail(DetailView):
    model = models.Entry
    template_name = 'post.html'
    context_object_name = 'entry'


def error404(request, exception):
    response = render(request, "404.html")
    response.status_code = 404
    return response


def error500(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response
