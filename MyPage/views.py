# -*- coding: utf-8 -*-
import simplejson
import datetime
import uuid
import base64

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, RequestContext, render
from django.contrib import auth
from django.contrib.auth.models import User
from MyPage.models import *


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

     return render(request, 'UserInfor.html', {'user': user, 'userInfo': userkey})


def photo(request):
     return render_to_response('Image.html')


# mobile login--------------------------------------------
@csrf_exempt
def mobileRegister(request):

    if request.method == 'POST':
        username = request.POST['newUserId']
        password = request.POST['newUserPassWord']

        a = User.objects.get(username=username)

        if a is not None:
            result = {'result': 0, 'accessToken': '', 'errorCode': 'User exist'}
            return HttpResponse(simplejson.dumps(result), 'application/json')

        else:
            user = User.objects.create_user(username=username, password=password)
            token = str(uuid.uuid4())
            custom = UserKey(user=user, token=token)
            custom.save()
            if user is not None:
                result = {'result': 1, 'accessToken': custom.token, 'errorCode': 'Success'}
                return HttpResponse(simplejson.dumps(result), 'application/json')

    else:
        result = {'result': 0, 'accessToken': '', 'errorCode': 'Post Not Coming'}
        return HttpResponse(simplejson.dumps(result), 'application/json')




        # try:
        #     User.objects.get(username=username)
        #     result = {'result': 0, 'accessToken': '', 'errorCode': 'User exist'}
        #     return HttpResponse(simplejson.dumps(result), 'application/json')
        #
        # except :
        #     user = User.objects.create_user(username=username, password=password)
        #     token = str(uuid.uuid4())
        #     # token = (uuid.uuid4())
        #     # token = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        #     custom = UserKey(user=user, token=token)
        #     custom.save()
        #
        #     if user is not None:
        #         result = {'result': 1, 'accessToken': custom.token, 'errorCode': 'Success'}
        #         return HttpResponse(simplejson.dumps(result), 'application/json')





@csrf_exempt
def mobileLogin(request):

    if request.method == 'POST':
         #Get Parameter

        user_id = request.POST['newUserId']
        user_password = request.POST['newUserPassWord']
        access_token = request.POST['accessToken']

        if access_token:
            # 토큰으로 정보 불러오기
            obj = UserKey.objects.get(token=access_token)
            oobj = obj.user
            user_id = oobj.username
            user_password = oobj.password
            user = auth.authenticate(username=user_id, password=user_password)
            if user is not None:
                # token = uuid.uuid4()
                token = str(uuid.uuid4())
                obj.__dict__.update(user=user, token=token)
                # obj.save()
                user_token = UserKey.objects.get(user=user).token

                result = {'result': 1, 'accessToken': user_token, 'errorCode': 'accessToken exist'}
                return HttpResponse(simplejson.dumps(result), 'application/json')
            else:
                result = {'result': 0, 'accessToken': '', 'errorCode': 'UserNone'}
                return HttpResponse(simplejson.dumps(result), 'application/json')

        else:
            user = auth.authenticate(username=user_id, password=user_password)
            if user is not None:
                # token = uuid.uuid4()
                token = str(uuid.uuid4())
                obj = UserKey.objects.get(user=user)
                obj.__dict__.update(user=user, token=token)
                # obj.save()

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


# ----------------------------------------------------------------------------------
def check(request):

    # 한번은 그냥되게



    # 두번일경우는 로그인 싸인



    # 로그인 했을 경우 가능
    if request.method == 'POST':
        result = {'Message': 'Success'}
        return HttpResponse(simplejson.dumps(result), 'application/json')
    else:
        result = {'Message': 'Fail'}
        return HttpResponse(simplejson.dumps(result), 'application/json')



# def mobileLogin(request):
#     if request.method == 'POST':
#         user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
#         if user is not None:
#             if user.is_active:
#                 .get(user=user)
#                     result = {'result': 1, 'accessToken': token.token, 'errorCode': TOKEN_EXIST}
#                     return HttpResponse(simplejson if UserKey.objects.filter(user=user).count() != 0:
#                     token = UserKey.objects.dumps(result), 'application/json')
#
#                 token = UserKey.objects.create(user)
#                 result = {'result': 1, 'accessToken': token.key, 'errorCode': SUCCESS_CODE}
#                 return HttpResponse(simplejson.dumps(result), 'application/json')
#
#             else:
#                 result = {'result': 0, 'accessToken': '', 'errorCode': USER_NOT_ACTIVE}
#                 return HttpResponse(simplejson.dumps(result), 'application/json')
#         else:
#             result = {'result': 0, 'accessToken': '', 'errorCode': AUTHENTICATION_FAIL}
#             return HttpResponse(simplejson.dumps(result), 'application/json')
#
#     else:
#         return render_to_response('UserInfor.html', RequestContext(request))