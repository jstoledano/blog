# coding: utf-8

#         app: org.toledano.blogApp
#      module: blog.urls
# description: URL patterns form blog app
#      author: Javier Sanchez Toledano
#        date: 2022-08-20
#     licence: MIT
#      python: 3.10

from django.urls import path
from django.contrib.sitemaps.views import sitemap

from . import views
from .sitemaps import BlogSitemap

sitemaps = {
    'blog': BlogSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('blog/', views.BlogIndex.as_view(), name='blogIndex'),
    path('category/', views.CategoryList.as_view(), name='category_list'),
    path('category/<str:slug>', views.CategoryDetail.as_view(), name='category_detail'),
    path('<str:category>/<str:slug>', views.EntryDetail.as_view(), name='entry'),
    path('', views.IndexView.as_view(), name='index'),
]
