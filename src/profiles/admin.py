# coding: utf-8

from authtools.admin import NamedUserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _('Profile')
    fk_name = 'user'


class UserAdmin(NamedUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('get_slug', 'email', 'name', 'is_staff', 'get_location')
    list_select_related = ('profile',)
    icon = '<i class="material-icons">face</i>'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

    def get_location(self, user):
        return user.profile.location

    def get_slug(self, user):
        return user.profile.slug

    get_location.short_description = 'Ubicación'
    get_slug.short_description = 'Usuario'


admin.site.register(User, UserAdmin)
