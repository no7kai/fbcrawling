from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200)
    uid = models.CharField(max_length=100, unique=True)
    followers = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    postid = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField('created time')
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    hashtag = models.TextField()

    def __str__(self):
        return self.postid

    class Meta:
        ordering = ['-created']
