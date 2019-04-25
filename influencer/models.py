from django.db import models


class Influencer(models.Model):
    name = models.CharField(max_length=200) # => Maybe first name and last name, 2 fields
    uid = models.CharField(max_length=100, unique=True)
    followers = models.IntegerField(default=0)

    def __str__(self):
        return "{} - {}".format(self.name, self.uid)


class Post(models.Model):
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    message = models.TextField()
    postid = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField()
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    hashtag = models.TextField()

    def __str__(self):
        return self.postid

    class Meta:
        ordering = ['-created']
