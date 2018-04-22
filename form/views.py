import json

from django import shortcuts
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from . import models


def article_list(request):
    l = list()
    articles = models.Article.objects.all()
    for article in articles:
        vote = models.VoteArticle.objects.filter(article__id=article.id).count()
        comment = models.ArticleComment.objects.filter(article__id=article.id).count()
        l.append({'id': article.id, 'title': article.title, 'vote': vote, 'comment': comment, 'content': article.content})
    data = {'name': 'list', 'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def discussion_list(request):
    l = list()
    discussions = models.Discussion.objects.all()
    for discussion in discussions:
        vote = models.VoteDiscussion.objects.filter(discussion__id=discussion.id).count()
        comment = models.DiscussionComment.objects.filter(discussion_id=discussion.id).count()
        area_discussion = models.AreaDiscussion.objects.filter(discussion__id=discussion.id)
        spot_discussion = models.SpotDiscussion.objects.filter(discussion__id=discussion.id)
        title = ''
        if area_discussion.count():
            title = area_discussion[0].area.name
        elif spot_discussion.count():
            title = spot_discussion[0].spot.name
        l.append({'id': discussion.id, 'title': title, 'vote': vote, 'comment': comment, 'content': discussion.content})

    data = {'name': 'list', 'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def article_detail(request, article_id):
    data = {'err': '文章不存在'}
    article = models.Article.objects.get(id=article_id)

    user = None
    if request.user.is_authenticated:
        user = request.user
    if not article:
        return HttpResponse(json.dumps(data), content_type='application/json')

    votes = models.VoteArticle.objects.filter(article__id=article.id)
    comment = models.ArticleComment.objects.filter(article__id=article.id).count()
    voted = 0
    if user:
        voted = votes.filter(user=user).count()
    result = {'id': article.id, 'title': article.title, 'vote': votes.count(), 'comment': comment,
              'author': article.user.username, 'voted': voted, 'content': article.content}
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


# ----------------------------------------------------------
def discussion_detail(request, discussion_id):
    data = {'err': '文章不存在'}
    discussion = models.Discussion.objects.get(id=discussion_id)

    user = None
    if request.user.is_authenticated:
        user = request.user
    if not discussion:
        return HttpResponse(json.dumps(data), content_type='application/json')

    votes = models.VoteDiscussion.objects.filter(discussion__id=discussion.id)
    comment = models.DiscussionComment.objects.filter(discussion__id=discussion.id).count()
    area_discussion = models.AreaDiscussion.objects.filter(discussion__id=discussion.id)
    spot_discussion = models.SpotDiscussion.objects.filter(discussion__id=discussion.id)
    title = ''
    if area_discussion.count():
        title = area_discussion[0].area.name
    elif spot_discussion.count():
        title = spot_discussion[0].spot.name
    voted = 0
    if user:
        voted = votes.filter(user=user).count()
    result = {'id': discussion.id, 'title': title, 'vote': votes.count(), 'comment': comment,
              'author': discussion.user.username, 'voted': voted, 'content': discussion.content}
    data = {'obj': result}
    return HttpResponse(json.dumps(data), content_type='application/json')


def have_logined(request):
    user = None
    result = {'userName': '', 'userId': 0}
    if request.user.is_authenticated:
        user = request.user
    if user:
        result = {'userName': user.username, 'userId': user.id}
    data = {'obj': result}
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
            auth.login(request, user)

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
            auth.login(request, user)

            user = {'userName': user.username, 'userId': user.id}
            data = {'obj': user}
            return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse(json.dumps(data), content_type='application/json')


def logout(request):
    auth.logout(request)

    user = {'userName': '', 'userId': 0}
    data = {'obj': user}
    return HttpResponse(json.dumps(data), content_type='application/json')
