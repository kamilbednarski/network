from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followed_by_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "content": self.content,
            "timestamp": self.timestamp
        }

    def __str__(self):
        return "post with id: " + str(self.id) + " from user: " + str(self.user)


class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "user with id: " + str(self.user_id) + " likes post with id: " + str(self.post_id)


class Relation(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend_id = models.ManyToManyField(User, related_name='friend')

    def __str__(self):
        return "user with id: " + str(self.user_id) + " follows user with id: " + str(self.friend_id)