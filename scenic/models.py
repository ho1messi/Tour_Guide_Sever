from django.db import models


class ScenicArea(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    about = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class ScenicSpot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    area = models.ForeignKey(ScenicArea, on_delete=models.CASCADE)
    about = models.TextField()

    def __str__(self):
        return self.name

