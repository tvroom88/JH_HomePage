from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save




class UserInformation(models.Model):
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=80)

class UserInformationAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(UserInformation, UserInformationAdmin)

class VoteInfo(models.Model):
    image_url = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now=True)
    vote = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return self.image_url + "  " + self.vote

    def __unicode__(self):
        return self.image_url + "  " + self.vote

class VoteInfoAdmin(admin.ModelAdmin):
    list_display = ('image_url', 'created', 'vote')

admin.site.register(VoteInfo, VoteInfoAdmin)


class UserKey(models.Model):
    user = models.OneToOneField(User)
    token = models.CharField(max_length=255)
    votes = models.ManyToManyField('VoteInfo', related_name='vote_information', blank=True)
    registrationId = models.CharField(max_length=255)

    def get_vote(self):
        return "\n".join([p.image_url for p in self.votes.all()])

    def get_votes(self):
        return self.votes.all()

class UserKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'get_votes', 'registrationId')


admin.site.register(UserKey, UserKeyAdmin)

