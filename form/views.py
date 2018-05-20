import json

from django import shortcuts
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from . import models
from scenic import models as smodels


def article_list(request):
    l = list()
    articles = models.Article.objects.all()
    for article in articles:
        vote = models.VoteArticle.objects.filter(article__id=article.id).count()
        comment = models.ArticleComment.objects.filter(article__id=article.id).count()
        l.append({'id': article.id, 'title': article.title, 'vote': vote, 'comment': comment,
                  'content': article.content[:80]})
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
        l.append({'id': discussion.id, 'title': title, 'vote': vote, 'comment': comment,
                  'content': discussion.content[:80]})

    data = {'name': 'list', 'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def article_comment_list(request, article_id):
    l = list()
    article_comments = models.ArticleComment.objects.filter(article__id=article_id)
    for article_comment in article_comments:
        comment = article_comment.comment
        l.append({'name': comment.user.username, 'id': comment.id, 'content': comment.content})

    data = {'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def discussion_comment_list(request, discussion_id):
    l = list()
    discussion_comments = models.DiscussionComment.objects.filter(discussion__id=discussion_id)
    for discussion_comment in discussion_comments:
        comment = discussion_comment.comment
        l.append({'name': comment.user.username, 'id': comment.id, 'content': comment.content})

    data = {'obj': l}
    return HttpResponse(json.dumps(data), content_type='application/json')


def area_article_list(request, area_id):
    l = list()
    area = smodels.ScenicArea.objects.get(id=area_id)
    area_articles = models.AreaArticle.objects.filter(area__id=area_id)
    for area_article in area_articles:
        article = area_article.article
        vote = models.VoteArticle.objects.filter(article__id=article.id).count()
        comment = models.ArticleComment.objects.filter(article__id=article.id).count()
        l.append({'id': article.id, 'title': article.title, 'vote': vote, 'comment': comment,
                  'content': article.content[:80]})
    data = {'name': 'list', 'obj': {
        'name': area.name, 'id': area.id, 'objects': l,
    }}
    return HttpResponse(json.dumps(data), content_type='application/json')


def area_discussion_list(request, area_id):
    l = list()
    area = smodels.ScenicArea.objects.get(id=area_id)
    area_discussions = models.AreaDiscussion.objects.filter(area__id=area_id)
    for area_discussion in area_discussions:
        discussion = area_discussion.discussion
        vote = models.VoteDiscussion.objects.filter(discussion__id=discussion.id).count()
        comment = models.DiscussionComment.objects.filter(discussion_id=discussion.id).count()
        area_discussion_t = models.AreaDiscussion.objects.filter(discussion__id=discussion.id)
        spot_discussion_t = models.SpotDiscussion.objects.filter(discussion__id=discussion.id)
        title = ''
        if area_discussion_t.count():
            title = area_discussion_t[0].area.name
        elif spot_discussion_t.count():
            title = spot_discussion_t[0].spot.name
        l.append({'id': discussion.id, 'title': title, 'vote': vote, 'comment': comment,
                  'content': discussion.content[:80]})

    data = {'name': 'list', 'obj': {
        'name': area.name, 'id': area.id, 'objects': l,
    }}
    return HttpResponse(json.dumps(data), content_type='application/json')


def spot_article_list(request, spot_id):
    l = list()
    spot = smodels.ScenicSpot.objects.get(id=spot_id)
    spot_articles = models.SpotArticle.objects.filter(spot__id=spot_id)
    for spot_article in spot_articles:
        article = spot_article.article
        vote = models.VoteArticle.objects.filter(article__id=article.id).count()
        comment = models.ArticleComment.objects.filter(article__id=article.id).count()
        l.append({'id': article.id, 'title': article.title, 'vote': vote, 'comment': comment,
                  'content': article.content[:80]})
    data = {'name': 'list', 'obj': {
        'name': spot.name, 'id': spot.id, 'objects': l,
    }}
    return HttpResponse(json.dumps(data), content_type='application/json')


def spot_discussion_list(request, spot_id):
    l = list()
    spot = smodels.ScenicSpot.objects.get(id=spot_id)
    spot_discussions = models.SpotDiscussion.objects.filter(spot__id=spot_id)
    for spot_discussion in spot_discussions:
        discussion = spot_discussion.discussion
        vote = models.VoteDiscussion.objects.filter(discussion__id=discussion.id).count()
        comment = models.DiscussionComment.objects.filter(discussion_id=discussion.id).count()
        area_discussion_t = models.AreaDiscussion.objects.filter(discussion__id=discussion.id)
        spot_discussion_t = models.SpotDiscussion.objects.filter(discussion__id=discussion.id)
        title = ''
        if area_discussion_t.count():
            title = area_discussion_t[0].area.name
        elif spot_discussion_t.count():
            title = spot_discussion_t[0].spot.name
        l.append({'id': discussion.id, 'title': title, 'vote': vote, 'comment': comment,
                  'content': discussion.content[:80]})

    data = {'name': 'list', 'obj': {
        'name': spot.name, 'id': spot.id, 'objects': l,
    }}
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


def publish_article(request):
    data = {'err': '发布失败'}

    if request.method == 'POST':
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps(data), content_type='application/json')
        user = request.user
        if user and title and content:
            article = models.Article(user=user, title=title, content=content)
            article.save()
            area_id = request.POST.get('area', None)
            spot_id = request.POST.get('spot', None)
            if area_id:
                area = smodels.ScenicArea.objects.get(id=area_id)
                if area:
                    models.AreaArticle.objects.create(article=article, area=area)
            if spot_id:
                spot = smodels.ScenicSpot.objects.get(id=spot_id)
                if spot:
                    models.SpotArticle.objects.create(article=article, spot=spot)

            data = {'obj': {'id': article.id}}

    return HttpResponse(json.dumps(data), content_type='application/json')


def publish_discussion(request):
    data = {'err': '发布失败'}

    if request.method == 'POST':
        content = request.POST.get('content', None)
        if not request.user.is_authenticated:
            return HttpResponse(json.dumps(data), content_type='application/json')
        user = request.user
        if user and content:
            discussion = models.Discussion(user=user, content=content)
            discussion.save()
            area_id = request.POST.get('area', None)
            spot_id = request.POST.get('spot', None)
            if area_id:
                area = smodels.ScenicArea.objects.get(id=area_id)
                models.AreaDiscussion.objects.create(discussion=discussion, area=area)
            if spot_id:
                spot = smodels.ScenicSpot.objects.get(id=spot_id)
                models.SpotDiscussion.objects.create(discussion=discussion, spot=spot)

            data = {'obj': {'id': discussion.id}}

    return HttpResponse(json.dumps(data), content_type='application/json')


def publish_comment(request):
    data = {'err': '发布失败'}

    if request.method != 'POST':
        return HttpResponse(json.dumps(data), content_type='application/json')
    if not request.user.is_authenticated:
        data = {'err': '请先登录'}
        return HttpResponse(json.dumps(data), content_type='application/json')

    user = request.user
    content = request.POST.get('content', None)
    comment = models.Comment(content=content, user=user)
    comment.save()

    article_id = request.POST.get('article', None)
    discussion_id = request.POST.get('discussion', None)
    if article_id:
        article = models.Article.objects.get(id=article_id)
        models.ArticleComment.objects.create(article=article, comment=comment)
    if discussion_id:
        discussion = models.Discussion.objects.get(id=discussion_id)
        models.DiscussionComment.objects.create(discussion=discussion, comment=comment)

    data = {'obj': {'id': comment.id, 'user': {'id': user.id, 'name': user.username}}}
    return HttpResponse(json.dumps(data), content_type='application/json')


def publish_vote(request):
    data = {'err': '点赞失败'}

    if request.method != 'POST':
        return HttpResponse(json.dumps(data), content_type='application/json')
    if not request.user.is_authenticated:
        data = {'err': '请先登录'}
        return HttpResponse(json.dumps(data), content_type='application/json')

    user = request.user
    article_id = request.POST.get('article', None)
    discussion_id = request.POST.get('discussion', None)

    if article_id:
        article = models.Article.objects.get(id=article_id)
        votes = models.VoteArticle.objects.filter(article=article, user=user)
        if len(votes):
            votes[0].delete()
        else:
            models.VoteArticle.objects.create(article=article, user=user)
    if discussion_id:
        discussion = models.Discussion.objects.get(id=discussion_id)
        votes = models.VoteDiscussion.objects.filter(discussion=discussion, user=user)
        if len(votes):
            votes[0].delete()
        else:
            models.VoteDiscussion.objects.create(discussion=discussion, user=user)

    data = {'obj': '点赞成功'}
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
