import json

from django import shortcuts
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from . import models


def article_list(request):
    l = list()
    for i in range(7):
        l.append({'id': i, 'title': 'title %d' % (i + 1), 'vote': i * 5, 'comment': i * 2,
                  'content': 'texttexttexttexttexttexttexttexttexttexttexttexttexttext'})
    articles = models.Article.objects.all()
    for article in articles:
        pass
        # l.append({'id': article.id, 'title': article.title, 'favor'})
    data = {'name': 'list', 'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def discussion_list(request):
    l = list()
    for i in range(10):
        l.append({'id': i, 'title': 'spot %d' % i, 'vote': i * 5, 'comment': i * 2,
                  'content': 'commentcommentcommentcommentcommentcommentcommentcommentcomment'})
    data = {'name': 'list', 'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def article_detail(request, article_id):
    article = shortcuts.get_object_or_404(models.Article, pk=1)
    result = {'id': article.id, 'title': article.title, 'vote': 3, 'comment': 0, 'author': article.user.username,
              'voted': True, 'content': article.content}
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


def discussion_detail(request, article_id):
    article = {'id': article_id, 'title': 'spot %d' % article_id, 'vote': article_id * 5, 'comment': article_id * 3,
               'author': 'aaa', 'voted': False, 'content': 'comment'}
    for i in range(70):
        article['content'] += '\ncomment'
    article['content'] += '\nend'
    data = {'obj': article}
    return HttpResponse(json.dumps(data), content_type='application/json')


def have_logined(request):
    result = request.session.get('username', '')
    print(result)
    # -------------------------------------------------------------
    id = 0
    user = {'userName': result, 'userId': id}
    data = {'name': 'result', 'obj': user}
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

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except Exception as e:
            data = {'err': e.__str__()}
        else:
            request.session['username'] = username
            auth.login(request, user)

            # -------------------------------------------------------------
            user = {'userName': username, 'userId': user.id}
            data = {'name': 'result', 'obj': user}
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

            # -------------------------------------------------------------
            user = {'userName': username, 'userId': user.id}
            data = {'obj': user}
            return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse(json.dumps(data), content_type='application/json')


def logout(request):
    auth.logout(request)

    user = {'userName': '', 'userId': 0}
    data = {'obj': user}
    return HttpResponse(json.dumps(data), content_type='application/json')
