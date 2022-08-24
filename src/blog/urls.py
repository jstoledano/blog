# coding: utf-8

#         app: org.toledano.blogApp
#      module: blog.urls
# description: URL patterns form blog app
#      author: Javier Sanchez Toledano
#        date: 2022-08-20
#     licence: MIT
#      python: 3.10

from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.CategoryList.as_view(), name='category_list'),
    path('category/<str:slug>', views.CategoryDetail.as_view(), name='category_detail'),
    path('<str:category>/<str:slug>', views.EntryDetail.as_view(), name='entry_detail'),
]
