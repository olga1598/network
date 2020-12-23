from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime 


class User(AbstractUser):
    created = models.DateTimeField(default=datetime.now, blank=True)
    # MayToManyField for SELF
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")

    def __str__(self):
        return f"{self.username}"


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete = models.PROTECT, related_name="comment_user")
    post = models.TextField(blank=False)
    created = models.DateTimeField(default=datetime.now, blank=True)
    likes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.id}: post by {self.creator}"

# class Follower(models.Model):
#     following = models.ManyToManyField(User, blank=True, related_name="followers")


# class Profile(models.Model):
#     user = models.ForeignKey(User, on_delete = models.CASCADE)
#     following = models.ManyToManyField(User, blank=True, related_name="followers")

#     def __str__(self):
#         return f"{self.id}: {self.following}"
