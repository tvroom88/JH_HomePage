from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save



class FBlogin(models.Model):
    user_id = models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=80)

    def __str__(self):
        return self.user_id

class FBloginAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'password')

admin.site.register(FBlogin, FBloginAdmin)

class VoteInfo(models.Model):
    image_url = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.image_url

    def __unicode__(self):
        return self.image_url

class VoteInfoAdmin(admin.ModelAdmin):
    list_display = ('image_url', 'created')

class Token(models.Model):
    fb_user = models.OneToOneField(FBlogin)
    token = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now=True)
    votes = models.ManyToManyField(VoteInfo, blank=True)

    def __str__(self):
        return self.token

    def get_vote(self):
        return "\n".join([p.image_url for p in self.votes.all()])

class TokenAdmin(admin.ModelAdmin):
    list_display = ('fb_user', 'token', 'created', 'get_vote')

admin.site.register(Token, TokenAdmin)



admin.site.register(VoteInfo, VoteInfoAdmin)


class UserKey(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=255)
    votes = models.ManyToManyField('VoteInfo', related_name='vote_information', blank=True)

    def get_vote(self):
        return "\n".join([p.image_url for p in self.votes.all()])

    def get_votes(self):
        return self.votes.all()

class UserKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'get_votes')


admin.site.register(UserKey, UserKeyAdmin)

