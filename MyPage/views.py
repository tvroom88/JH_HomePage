# -*- coding: utf-8 -*-
import json
import simplejson
import datetime
import uuid
import requests
import base64

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, RequestContext, render
from django.contrib import auth
from django.contrib.auth.models import User
from MyPage.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse


# ---------------------------------------
from django.core import serializers


# Create your views here.

@csrf_exempt
def main_page(request):
    # return render_to_response('main_page.html')
    return render_to_response('main_page.html', RequestContext(request, {'id': 1}))

@csrf_exempt
def hello(request):
    return HttpResponse("hi")


@csrf_exempt
def current_datetime(request):

    now = datetime.datetime.now()
    item = {"jaehong","jaehoon","mother","father"}
    return render(request, 'current_datetime.html', {'current_date': now, 'item': item})


@csrf_exempt
def Join(request):
    return render_to_response('JoinNewPeople.html', RequestContext(request, {'id': 1}))


@csrf_exempt
def register(request):

    if request.method == 'POST':
        username = request.POST['newUserId']
        password = request.POST['newUserPassWord']
        try:
            User.objects.get(username=username)
            return HttpResponse("이미 있는 아이디 입니다")
        except:
            users = User.objects.create_user(username=username, password=password)
            token = uuid.uuid4()
            custom = UserKey(user=users, token=token)
            custom.save()


            if users is not None:
                return HttpResponseRedirect('/')

#--------------------------------------------------
@csrf_exempt
def login_page(request):
     return render_to_response('login_page.html', RequestContext(request, {'id': 1}))


@csrf_exempt
def login(request):
    #Get Parameter
    user_id = request.POST['user_id']
    user_password = request.POST['user_password']

    # print user_id
    # print user_password
    user = auth.authenticate(username=user_id, password=user_password)

    if user is not None:
        auth.login(request, user)
        # users = User.objects.get(username=user_id)
        token = uuid.uuid4()

        try:
            obj = UserKey.objects.get(user=user)
        except UserKey.DoesNotExist:
            obj = UserKey.objects.create()
        obj.__dict__.update(user=user, token=token)
        obj.save()

        return HttpResponseRedirect('/')
    else:
        result = {'result': '0', 'accessToken': ''}
        return HttpResponse(simplejson.dumps(result), 'application/json')

# 로그아웃할때 main_page로 돌가가게 함
@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def userInformation(request):
     user = User.objects.all()
     userkey = UserKey.objects.filter()
     regId = UserKey.objects.values_list('registrationId', flat=True)


     return render(request, 'UserInfor.html', {'user': user, 'userInfo': userkey, 'regId': regId})


def photo(request):
     return render_to_response('Image.html')


# mobile login--------------------------------------------
@csrf_exempt
def mobileRegister(request):

    if request.method == 'POST':
        username = request.POST['newUserId']
        password = request.POST['newUserPassWord']
        post = User.objects.filter(username=username)

        if post:
            result = {'result': 0, 'accessToken': '', 'errorCode': 'User exist'}
            return HttpResponse(simplejson.dumps(result), 'application/json')
        else:
            user = User.objects.create_user(username=username, password=password)
            user_key = UserKey(user=user)
            user_key.save()

            result = {'result': 1, 'errorCode': 'Success'}
            return HttpResponse(simplejson.dumps(result), 'application/json')

    else:
        result = {'result': 0, 'accessToken': '', 'errorCode': 'Post Not Coming'}
        return HttpResponse(simplejson.dumps(result), 'application/json')

@csrf_exempt
def mobileLogin(request):
    if request.method == 'POST':
         #Get Parameter
        accessToken = request.POST['accessToken']
        token = str(uuid.uuid4())

        # Token.objects.filter(user=user).count() != 0:
                    # token = Token.objects.get(user=user)
                    # result = {'result': 1, 'accessToken': token.key, 'errorCode': TOKEN_EXIST}
                    # return HttpResponse(simplejson.dumps(result), 'application/json')

        # obj = UserKey.objects.get(token=accessToken)
        # if accessToken:
        # UserKey.objects.filter(token=accessToken)
        if UserKey.objects.filter(token=accessToken).count() != 0:
            # 토큰으로 정보 불러오기
            obj = UserKey.objects.get(token=accessToken)
            info_object = obj.user
            user_id = info_object.username
            user_password = info_object.password

            print user_id
            print user_password

            # user = auth.authenticate(username=user_id, password=user_password)
            user = User.objects.filter(username=user_id, password=user_password)
            if user is not None:

                obj.__dict__.update(user=user, token=token)
                obj.save()
                user_token = UserKey.objects.get(user=user).token

                result = {'result': 1, 'accessToken': user_token, 'errorCode': 'accessToken exist'}
                return HttpResponse(simplejson.dumps(result), 'application/json')
            else:
                result = {'result': 0, 'accessToken': '', 'errorCode': 'UserNone'}
                return HttpResponse(simplejson.dumps(result), 'application/json')
        else:
            user = auth.authenticate(username=request.POST['newUserId'], password=request.POST['newUserPassWord'])
            if user is not None:
                # token = str(uuid.uuid4())
                obj = UserKey.objects.get(user=user)
                obj.__dict__.update(user=user, token=token)
                obj.save()

                user_token = obj.token

                result = {'result': 1, 'accessToken': user_token, 'errorCode': 'accessToken None, id password exist'}
                return HttpResponse(simplejson.dumps(result), 'application/json')
            else:
                result = {'result': 0, 'accessToken': '', 'errorCode': 'UserNone'}
                return HttpResponse(simplejson.dumps(result), 'application/json')

    # POST가 아닐경우?
    else:
        result = {'result': 0, 'accessToken': '',  'errorCode': 'Fail'}
        return HttpResponse(simplejson.dumps(result), 'application/json')

@csrf_exempt
def a(request):
    leads_as_json = serializers.serialize('json', User.objects.all())
    return HttpResponse(simplejson.dumps(leads_as_json), 'application/json')


@csrf_exempt
def fblogin(request):
    if request.method == 'POST':
        username = request.POST['newUserId']
        password = request.POST['newUserPassWord']
        user_token = request.POST['accessToken']

        newToken = str(uuid.uuid4())

        try:
            # 유저가 존재할경우 유저정보 가져오기
            userExist = FBlogin.objects.filter(user_id=username)

            # 모바일에서 토큰이 잘 온다면
            if user_token:

                # 토큰은 잘왔지만 토큰이 저장되있는 토큰과 다를경우
                update_token = Token.objects.get(fb_user=userExist)

                if update_token.token == user_token:
                    update_token.__dict__.update(token=newToken)
                    update_token.save()

                else:
                    update_token = Token.objects.get(fb_user=userExist)


            # 유저가 존재하지만 token이 안올경우
            else:
                update_token = Token.objects.get(fb_user=userExist)

            sendToken = update_token.token


            result = {'result': 1, 'accessToken': sendToken, 'errorCode': 'UserExist, Change token'}
            return HttpResponse(simplejson.dumps(result), 'application/json')
        except:
            # 유저정보가 없다면 유저 저장해주고
            newUser = FBlogin(user_id=username, password=password)
            newUser.save()

            # 토큰모델에도 저장해줌
            newUserToken = Token(fb_user=newUser, token=newToken)
            newUserToken.save()

            # 그다음 유저 아이디랑 패스워드 토큰을 같이 저장해준다

            result = {'result': 1, 'accessToken': newUserToken.token, 'errorCode': 'makeUser'}
            return HttpResponse(simplejson.dumps(result), 'application/json')
    else:
        result = {'result': 0, 'accessToken': '', 'errorCode': 'UserNone'}
        return HttpResponse(simplejson.dumps(result), 'application/json')






@csrf_exempt
def auction(request):
    if request.method == 'POST':
        accessToken = request.POST['accessToken']
        onclick = request.POST['onclick']
        url = request.POST['url']


        if onclick == 'onclick':
                # obj = VoteInfo.objects.get(id=1)
            # onclick이 눌려진다면 토큰에 눌렀다는 정보 넣어주기

            userInfo = Token.objects.get(token=accessToken)
            obj = VoteInfo.objects.get(image_url=url)

            try:
                a = userInfo.votes.get(image_url=obj)
                msg = 0
            except:
                userInfo.votes.add(obj)
                msg = 1

            result = {'imageUrl': obj.image_url, 'created': obj.created, 'msg': msg}
            return HttpResponse(json.dumps(result, cls=DjangoJSONEncoder), 'application/json')

        else:
            objs = VoteInfo.objects.all()
            dic = []
            for a in objs:
                result = {
                'imageUrl': a.image_url,
                'created': a.created,
                }
                dic.append(result)
            return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), 'application/json')

    else:

        # voteValue = Vote.objects.all().values()
        # results = serializers.serialize('json', voteValue)
        # result = serializers.serialize('json', VoteInfo.objects.all())
        voteinfo = VoteInfo.objects.all()
        dic = []
        for a in voteinfo:
            result = {
                'imageUrl': a.image_url,
                'created': a.created,
            }
            dic.append(result)

        return HttpResponse(json.dumps(dic, cls=DjangoJSONEncoder), 'application/json')
