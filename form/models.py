from django.db import models
from django.contrib.auth.models import User
from scenic.models import ScenicArea, ScenicSpot


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()


class AreaArticle(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class SpotArticle(models.Model):
    id = models.AutoField(primary_key=True)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class AreaDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)


class SpotDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()


class ArticleComment(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class DiscussionComment(models.Model):
    id = models.AutoField(primary_key=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)


class CommentComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_d = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='destination_comment')
    comment_s = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='source_comment')


class AreaScore(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'area')


class SpotScore(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'spot')


class FollowArea(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'area')


class FollowSpot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'spot')


class FollowUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_s = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source_user')
    user_d = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dest_user')

    class Meta:
        unique_together = ('user_s', 'user_d')


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)


class AreaTag(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('area', 'tag')


class SpotTag(models.Model):
    id = models.AutoField(primary_key=True)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('spot', 'tag')


class ArticleTag(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'tag')


class VoteArticle(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')


class VoteDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')
