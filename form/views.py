import json

from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

user = None


def article_view(request):
    l = list()
    for i in range(7):
        l.append({'id': i, 'title': 'title %d' % (i + 1), 'favor': i * 5, 'comment': i * 2,
                  'content': 'texttexttexttexttexttexttexttexttexttexttexttexttexttext'})
    data = {'name': 'list', 'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def comment_view(request):
    l = list()
    for i in range(10):
        l.append({'id': i, 'title': 'spot %d' % i, 'favor': i * 5, 'comment': i * 2,
                  'content': 'commentcommentcommentcommentcommentcommentcommentcommentcomment'})
    data = {'name': 'list', 'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def have_logined(request):
    result = request.session.get('username', None)
    data = {'name': 'result', 'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


def register(request):
    data = {'err': '注册失败'}

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if not username:
            return HttpResponse(json.dumps(data), content_type='application/json')

        user = auth.authenticate(username=username, password=password)
        if user:
            data = {'err': '用户名已使用'}
            return HttpResponse(json.dumps(data), content_type='application/json')

        user = User.objects.create_user(username=username, password=password)
        user.save()

        request.session['username'] = username
        auth.login(request, user)

        data = {'obj': username}
        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse(json.dumps(data), content_type='application/json')


def login(request):
    data = {'err': '登录失败'}

    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        if not username:
            return HttpResponse(json.dumps(data), content_type='application/json')

        user = auth.authenticate(username=username, password=password)
        if user:
            request.session['username'] = username
            auth.login(request, user)
            data = {'obj': username}
            return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse(json.dumps(data), content_type='application/json')


def logout(request):
    # if request.method == 'POST':
        # username = request.POST.get('username', None)

        # if not username:
            # print('aaaaaaa')
        # else:
    auth.logout(request)

    data = {'obj': None}
    return HttpResponse(json.dumps(data), content_type='application/json')
