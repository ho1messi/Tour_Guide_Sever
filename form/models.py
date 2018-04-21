from django.db import models
from django.contrib.auth.models import User
from scenic.models import ScenicArea, ScenicSpot


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title


class AreaArticle(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.area.__str__() + ' ' + self.article.__str__()


class SpotArticle(models.Model):
    id = models.AutoField(primary_key=True)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.spot.__str__() + ' ' + self.article.__str__()


class Discussion(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.__str__() + ' ' + self.id.__str__()


class AreaDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    def __str__(self):
        return self.area.__str__() + ' ' + self.discussion.__str__()


class SpotDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    def __str__(self):
        return self.spot.__str__() + ' ' + self.discussion.__str__()


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.user.__str__() + ' ' + self.id.__str__()


class ArticleComment(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.article.__str__() + ' ' + self.comment.__str__()


class DiscussionComment(models.Model):
    id = models.AutoField(primary_key=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return self.discussion.__str__() + ' ' + self.comment.__str__()


class CommentComment(models.Model):
    id = models.AutoField(primary_key=True)
    comment_d = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='destination_comment')
    comment_s = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='source_comment')

    def __str__(self):
        return self.comment_d.__str__() + ' ' + self.comment_s.__str__()


class AreaScore(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'area')

    def __str__(self):
        return self.area.__str__() + ' ' + self.user.__str__() + ' ' + self.score.__str__()


class SpotScore(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    score = models.IntegerField()

    class Meta:
        unique_together = ('user', 'spot')

    def __str__(self):
        return self.spot.__str__() + ' ' + self.user.__str__() + ' ' + self.score.__str__()


class FollowArea(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'area')

    def __str__(self):
        return self.area.__str__() + ' ' + self.user.__str__()


class FollowSpot(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'spot')

    def __str__(self):
        return self.spot.__str__() + ' ' + self.user.__str__()


class FollowUser(models.Model):
    id = models.AutoField(primary_key=True)
    user_s = models.ForeignKey(User, on_delete=models.CASCADE, related_name='source_user')
    user_d = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dest_user')

    class Meta:
        unique_together = ('user_s', 'user_d')

    def __str__(self):
        return self.user_d.__str__() + ' ' + self.user_s.__str__()


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    # unique --------------------------------------------
    name = models.CharField(unique=True, max_length=20)

    def __str__(self):
        return self.name


class AreaTag(models.Model):
    id = models.AutoField(primary_key=True)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('area', 'tag')

    def __str__(self):
        return self.area.__str__() + ' ' + self.tag.__str__()


class SpotTag(models.Model):
    id = models.AutoField(primary_key=True)
    spot = models.ForeignKey(ScenicSpot, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('spot', 'tag')

    def __str__(self):
        return self.spot.__str__() + ' ' + self.tag.__str__()


class ArticleTag(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('article', 'tag')

    def __str__(self):
        return self.article.__str__() + ' ' + self.tag.__str__()


class VoteArticle(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return self.article.__str__() + ' ' + self.user.__str__()


class VoteDiscussion(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'discussion')

    def __str__(self):
        return self.discussion.__str__() + ' ' + self.user.__str__()
