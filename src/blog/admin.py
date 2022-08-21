# -*- coding: UTF-8 -*-

#         app: org.toledano.blog
#      módulo: Administración
# descripción: Gestión del bog en el área administrativa
#       autor: Javier Sanchez Toledano
#       fecha: sábado, 29 de agosto de 2015

# Modulo de administración
from django.contrib import admin
from django.db import models

# Módulos de la aplicación
from .models import Entry, Category


class EntryAdmin(admin.ModelAdmin):     # pylint: disable=R0904
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ["title"]
    date_hierarchy = 'pub_date'
    list_display = ('title', 'category', 'pub_date')
    list_filter = ('category', 'status')
    list_select_related = ('category',)
    icon = '<i class="material-icons">pages</i>'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class CategoryAdmin (admin.ModelAdmin):   # pylint: disable=R0904
    prepopulated_fields = {'slug': ['name']}
    icon = '<i class="material-icons">folder</i>'

    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Entry, EntryAdmin)
admin.site.register(Category, CategoryAdmin)
