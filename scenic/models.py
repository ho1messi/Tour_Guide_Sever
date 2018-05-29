from django.db import models


class ScenicArea(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    about = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class ScenicSpot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    about = models.TextField()
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    image = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name

