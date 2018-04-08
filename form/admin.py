from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Article)
admin.site.register(models.Comment)
admin.site.register(models.AreaScore)
admin.site.register(models.SpotScore)
admin.site.register(models.FollowSpot)
admin.site.register(models.FollowUser)
admin.site.register(models.Tag)
admin.site.register(models.ArticleTag)
admin.site.register(models.FavorArticle)
admin.site.register(models.FavorComment)

