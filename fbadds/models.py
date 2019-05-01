from django.db import models

# Create your models here.


class Page(models.Model):
    name = models.CharField(max_length=250)
    pageid = models.CharField(max_length=200, unique=True)


class Adds(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    addid = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    created_time = models.DateTimeField()
    likes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_time']
