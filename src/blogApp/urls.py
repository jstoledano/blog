from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView as t

import blog.views

urlpatterns = [
    path('robots.txt', t.as_view(template_name='extras/robots.txt', content_type='text/plain')),
    path('ads.txt', t.as_view(template_name='extras/ads.txt', content_type='text/plain')),
    path('BingSiteAuth.xml', t.as_view(template_name='extras/BingSiteAuth.xml', content_type='text/plain')),
    path('keybase.txt', t.as_view(template_name='extras/keybase.txt', content_type='text/plain')),
    path('', include(('blog.urls', 'blog'), namespace='blog')),
    path('admin/', admin.site.urls),
]
handler404 = 'blog.views.error404'
handler500 = 'blog.views.error500'
