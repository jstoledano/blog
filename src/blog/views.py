# coding: utf-8
#         app: org.toledano.blogApp
#      module: blog.views
# description: Views for blog app
#      author: Javier Sanchez Toledano
#        date: 2022-08-20
#     licence: MIT
#      python: 3.10

from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Model

from . import models


class CVView(TemplateView):
    template_name = 'resume.html'


class BlogIndex(ListView):
    queryset = models.Entry.objects.exclude(featured=True)[4:]
    template_name = 'index.html'
    context_object_name = 'entries'
    model = models.Entry
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sticky'] = models.Entry.objects.filter(featured=True)[0]
        context['primeros'] = models.Entry.objects.filter(featured=False)[:4]
        context['featured'] = models.Entry.objects.filter(featured=True)[1:6]
        return context


class CategoryList(ListView):
    model = models.Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    paginate_by = 6


class CategoryDetail(ListView):
    model: Model = models.Entry
    template_name: str = 'category.html'
    context_object_name: str = 'entries'
    paginate_by: int = 6
    allow_empty: bool = True
    slug_field: str = 'slug'

    def get_queryset(self):
        return models.Entry.objects\
            .filter(category__slug=self.kwargs['slug'], status=models.Entry.LIVE_STATUS)\
            .select_related('category')\
            .order_by('-pub_date', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured'] = models.Entry.objects.filter(featured=True)[:5]
        context['category'] = models.Category.objects.get(slug=self.kwargs['slug'])
        return context


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


class Archivo(TemplateView):
    template_name = 'archivo.html'

    def get_context_data(self, **kwargs):
        ctx = super(Archivo, self).get_context_data(**kwargs)
        ctx['cats'] = models.Category.objects.all()
        ctx['entries'] = models.Entry.objects\
            .order_by('-pub_date', '-id')\
            .filter(status=models.Entry.LIVE_STATUS)
        return ctx
