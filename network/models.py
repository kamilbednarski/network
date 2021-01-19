import json
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    country = models.TextField(max_length=56, blank=True, null=True)
    followers_counter = models.PositiveIntegerField(default=0)
    watched_counter = models.PositiveIntegerField(default=0)
    posts_counter = models.PositiveIntegerField(default=0)

    def get_number_of_posts(self):
        '''Returns total number of posts published by user.'''
        return self.posts_counter

    def get_number_of_followers(self):
        '''Returns total number of users that follows this user.'''
        return self.followers_counter

    def get_number_of_users_followed_by_this_user(self):
        '''Returns total number of users followed by this user.'''
        return self.watched_counter

    def increment_number_of_posts(self):
        '''
        Increments value of counter, that counts total number of posts
        published by this user.
        '''
        self.posts_counter += 1

    def increment_number_of_followers(self):
        '''
        Increments value of counter, that counts total number of users
        following this user.
        '''
        self.followers_counter += 1

    def increment_number_of_users_followed_by_this_user(self):
        '''
        Increments value of counter, that counts total number of users
        followed by this user.
        '''
        self.watched_counter += 1

    def decrement_number_of_posts(self):
        '''
        Decrements value of counter, that counts total number of posts
        published by this user.
        '''
        self.posts_counter -= 1

    def decrement_number_of_followers(self):
        '''
        Decrements value of counter, that counts total number of users
        following this user.
        '''
        self.followers_counter -= 1

    def decrement_number_of_users_followed_by_this_user(self):
        '''
        Decrements value of counter, that counts total number of users
        followed by this user.
        '''
        self.watched_counter -= 1


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return ({
            "id": self.id,
            "user": User.objects.get(id=self.user_id).username,
            "user_id": self.user_id,
            "content": self.content,
            "date_added": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        })

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
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user')
    users_friend = models.ManyToManyField(User, related_name='friend')

    def get_user(self):
        '''Returns user that is followed by other user in this relation.'''
        return self.user

    def get_users_friend(self):
        '''Returns user that is following other user in this relation.'''
        users_friend = User.objects.get(id=self.id)
        return users_friend

    def __str__(self):
        return ("user: "
                + f"'{str(self.user)}'"
                + " follows user: "
                + f"'{str(self.get_users_friend())}'")
