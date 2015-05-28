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

class UserKey(models.Model):
    user = models.OneToOneField(User, unique=False)
    token = models.CharField(max_length=100, primary_key=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserKey.objects.get_or_create(user=instance)
#
# post_save.connect(create_user_profile, sender=User)

class UserKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')

admin.site.register(UserKey, UserKeyAdmin)


# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.get_or_create(user=instance)
