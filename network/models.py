from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followed_by_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    posts_count = models.PositiveIntegerField(default=0)

    def get_number_of_posts(self):
        return self.posts_count

    def get_number_of_followers(self):
        return self.followed_by_count

    def get_number_of_followed_by_user(self):
        return self.following_count


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
        return ("post with id: "
                + str(self.id)
                + " from user: "
                + f"'{str(self.user)}'")


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return ("user: "
                + f"'{str(self.user)}'"
                + " likes "
                + str(self.post))


class Relation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    users_friend = models.ManyToManyField(User, related_name='friend')

    def get_users_friend(self):
        users_friend = User.objects.get(id=self.id)
        return users_friend

    def __str__(self):
        return ("user: "
                + f"'{str(self.user)}'"
                + " follows user: "
                + f"'{str(self.get_users_friend())}'")