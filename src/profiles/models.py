# coding: utf-8

#         app: org.toledano.blog
#      module: profiles.models
# description: Custom user models for toledano.blog
#      author: Javier Sanchez Toledano
#        date: 19/08/2022
#     license: MIT

import uuid

from authtools.models import AbstractNamedUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractNamedUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=30, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.email


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
