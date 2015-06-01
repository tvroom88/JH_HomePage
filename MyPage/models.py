from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.
# class RoomInformation(models.Model):
#     name = models.CharField(max_length=30)
#     image = modelsCharFI(max_length=50)


class UserInformation(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=80)

class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(UserInformation, UserInformationAdmin)

class Vote(models.Model):
    image_url = models.URLField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    vote = models.CharField(max_length=80, blank=True)

class VoteAdmin(admin.ModelAdmin):
    list_display = ('image_url', 'created', 'vote')

admin.site.register(Vote, VoteAdmin)


class UserKey(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=100, primary_key=True)
    # vote = models.ManyToManyField(ImageUrl)


class UserKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

admin.site.register(UserKey, UserKeyAdmin)
