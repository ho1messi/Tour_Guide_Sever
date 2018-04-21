from django.contrib import admin
from . import models

# Register your models here.


admin.site.register(models.Article)
admin.site.register(models.AreaArticle)
admin.site.register(models.SpotArticle)
admin.site.register(models.Discussion)
admin.site.register(models.AreaDiscussion)
admin.site.register(models.SpotDiscussion)
admin.site.register(models.Comment)
admin.site.register(models.ArticleComment)
admin.site.register(models.DiscussionComment)
admin.site.register(models.CommentComment)
admin.site.register(models.AreaScore)
admin.site.register(models.SpotScore)
admin.site.register(models.FollowArea)
admin.site.register(models.FollowSpot)
admin.site.register(models.FollowUser)
admin.site.register(models.Tag)
admin.site.register(models.AreaTag)
admin.site.register(models.SpotTag)
admin.site.register(models.ArticleTag)
admin.site.register(models.VoteArticle)
admin.site.register(models.VoteDiscussion)

