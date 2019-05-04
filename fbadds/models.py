from django.db import models
from django.utils.text import slugify

# Create your models here.


class Page(models.Model):
    name = models.CharField(max_length=250)
    pageid = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def ads(self):
        return '{} ads'.format(self.adds_set.count())


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
