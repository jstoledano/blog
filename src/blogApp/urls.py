from django.contrib import admin
from django.urls import path, include

import blog.views

urlpatterns = [
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path('admin/', admin.site.urls),
]
handler404 = 'blog.views.error404'
handler500 = 'blog.views.error500'
