import re
import json
from django.test import TestCase
from network.models import User, Post, Like, Relation


class UserTestCase(TestCase):
    '''
    Tests for User model.
    '''
    def set_up_new_test_user(self):
        test_user = User.objects.create(
            username='testuser',
            email='testuser@testcase.com',
            password='testpassword'
        )


    def set_up_new_test_users(self):
        first_test_user = User.objects.create(
            username='firsttestuser',
            email='testuser1@testcase.com',
            password='testpassword'
        )

        second_test_user = User.objects.create(
            username='secondtestuser',
            email='testuser2@testcase.com',
            password='testpassword'
        )


    def test_users_were_correctly_created(self):
        '''
        Checks if users were created.
        '''
        self.set_up_new_test_users()
        first_test_user = User.objects.get(username='firsttestuser')
        second_test_user = User.objects.get(username='secondtestuser')


    def test_users_variables_have_correct_values(self):
        '''
        Checks if created users' variables have correct values.
        '''
        self.set_up_new_test_users()
        first_test_user = User.objects.get(username='firsttestuser')
        second_test_user = User.objects.get(username='secondtestuser')

        self.assertEqual(first_test_user.username, 'firsttestuser')
        self.assertEqual(second_test_user.username, 'secondtestuser')

        self.assertEqual(first_test_user.email, 'testuser1@testcase.com')
        self.assertEqual(second_test_user.email, 'testuser2@testcase.com')


    def test_users_posts_counter(self):
        '''
        Checks posts_counter variable
        and functions associated with that field:
        - 'get_number_of_posts'
        - 'increment_number_of_posts'
        - 'decrement_number_of_posts'
        '''
        self.set_up_new_test_user()
        test_user = User.objects.get(username='testuser')

        self.assertEqual(test_user.get_number_of_posts(), 0)

        test_user.increment_number_of_posts()
        self.assertEqual(test_user.get_number_of_posts(), 1)

        test_user.decrement_number_of_posts()
        self.assertEqual(test_user.get_number_of_posts(), 0)


    def test_users_watched_counter(self):
        '''
        Checks watched_counter variable
        and functions associated with that field:
        - 'get_number_of_followed_by_user'
        - 'increment_number_of_followed_by_user'
        - 'decrement_number_of_followed_by_user'
        '''
        self.set_up_new_test_user()
        test_user = User.objects.get(username='testuser')

        self.assertEqual(test_user.get_number_of_followed_by_user(), 0)

        test_user.increment_number_of_followed_by_user()
        self.assertEqual(test_user.get_number_of_followed_by_user(), 1)

        test_user.decrement_number_of_followed_by_user()
        self.assertEqual(test_user.get_number_of_followed_by_user(), 0)


    def test_users_followers_counter(self):
        '''
        Checks followers_counter variable
        and functions associated with that field:
        - 'get_number_of_followed_by_user'
        - 'increment_number_of_followed_by_user'
        - 'decrement_number_of_followed_by_user'
        '''
        self.set_up_new_test_user()
        test_user = User.objects.get(username='testuser')

        self.assertEqual(test_user.get_number_of_followers(), 0)

        test_user.increment_number_of_followers()
        self.assertEqual(test_user.get_number_of_followers(), 1)

        test_user.decrement_number_of_followers()
        self.assertEqual(test_user.get_number_of_followers(), 0)


class PostTestCase(TestCase):
    '''
    Tests for Post model.
    '''
    def set_up_new_test_user(self):
        test_user = User.objects.create(
            username='testuser',
            email='testuser@testcase.com',
            password='testpassword'
        )


    def set_up_new_test_post(self):
        self.set_up_new_test_user()
        test_user = User.objects.get(username='testuser')

        test_post = Post.objects.create(
            user=test_user,
            content='This is test content of test post.'
        )


    def test_post_was_correctly_created(self):
        '''
        Checks if post was created correctly.
        '''
        self.set_up_new_test_post()
        test_post = Post.objects.get(id=1)


    def test_posts_content_variable_has_correct_value(self):
        '''
        Checks if created post's content variable has correct value.
        '''
        self.set_up_new_test_post()
        test_post = Post.objects.get(id=1)

        self.assertEqual(test_post.content, 'This is test content of test post.')

    def test_posts_timestamp_is_valid(self):
        '''
        Checks if variable timestamp is valid timestamp.
        '''
        self.set_up_new_test_post()
        test_post = Post.objects.get(id=1)
        timestamp = str(test_post.timestamp)

        status = False
        if re.match('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', timestamp):
            status = True

        self.assertEqual(status, True)

    def test_posts_serialization_is_valid_json(self):
        '''
        Checks if serialize function of Post object returns valid JSON object
        '''
        self.set_up_new_test_post()
        test_post = Post.objects.get(id=1)
        json_response = test_post.serialize()

        is_valid_json_status = True
        try:
            json_response = json.loads(json_response)
        except ValueError:
            is_valid_json_status = False

        self.assertEqual(is_valid_json_status, True)