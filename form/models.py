from django.db import models
from django.contrib.auth.models import User
from scenic.models import ScenicArea, ScenicSpot


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    article_d = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_d = models.ForeignKey('self', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class AreaScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'area')


class SpotScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'spot')


class FollowSpot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'spot')


class FollowUser(models.Model):
    user_s = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source_user')
    user_d = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dest_user')

    class Meta:
        unique_together = ('user_s', 'user_d')


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'tag')


class FavorArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')


class FavorComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')
