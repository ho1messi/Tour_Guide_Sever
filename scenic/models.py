from django.db import models


class ScenicArea(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    # area =


class ScenicSpot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    position = models.CharField(max_length=10)
    image = models.ImageField()
    about = models.TextField()

