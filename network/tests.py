import re
import json
import unittest
from django.urls import reverse
from django.test import TestCase, Client
from network.models import User, Post, Like, Relation


class UserTestCase(TestCase):
    '''
    Tests for User model.
    '''

    def setUp(self):
        self.test_user = User.objects.create(
            username='testuser',
            email='testuser@testcase.com',
            password='testpassword'
        )
        self.first_test_user = User.objects.create(
            username='firsttestuser',
            email='testuser1@testcase.com',
            password='testpassword'
        )
        self.second_test_user = User.objects.create(
            username='secondtestuser',
            email='testuser2@testcase.com',
            password='testpassword'
        )

    def test_user_objects_were_correctly_created(self):
        '''
        Checks if users were created.
        '''
        first_test_user = User.objects.get(username='firsttestuser')
        second_test_user = User.objects.get(username='secondtestuser')

    def test_user_object_variables_have_correct_values(self):
        '''
        Checks if created users' variables have correct values.
        '''
        first_test_user = User.objects.get(username='firsttestuser')
        second_test_user = User.objects.get(username='secondtestuser')

        self.assertEqual(first_test_user.username, 'firsttestuser')
        self.assertEqual(second_test_user.username, 'secondtestuser')

        self.assertEqual(first_test_user.email, 'testuser1@testcase.com')
        self.assertEqual(second_test_user.email, 'testuser2@testcase.com')

    def test_user_object_posts_counter_variable_has_correct_values(self):
        '''
        Checks posts_counter variable
        and functions associated with that field:
        - 'get_number_of_posts'
        - 'increment_number_of_posts'
        - 'decrement_number_of_posts'
        '''
        test_user = User.objects.get(username='testuser')

        self.assertEqual(test_user.get_number_of_posts(), 0)

        test_user.increment_number_of_posts()
        self.assertEqual(test_user.get_number_of_posts(), 1)

        test_user.decrement_number_of_posts()
        self.assertEqual(test_user.get_number_of_posts(), 0)

    def test_user_object_watched_counter_variable_has_correct_values(self):
        '''
        Checks watched_counter variable
        and functions associated with that field:
        - 'get_number_of_users_followed_by_this_user'
        - 'increment_number_of_users_followed_by_this_user'
        - 'decrement_number_of_users_followed_by_this_user'
        '''
        test_user = User.objects.get(username='testuser')

        self.assertEqual(
            test_user.get_number_of_users_followed_by_this_user(), 0)

        test_user.increment_number_of_users_followed_by_this_user()
        self.assertEqual(
            test_user.get_number_of_users_followed_by_this_user(), 1)

        test_user.decrement_number_of_users_followed_by_this_user()
        self.assertEqual(
            test_user.get_number_of_users_followed_by_this_user(), 0)

    def test_user_object_followers_counter_variable_has_correct_values(self):
        '''
        Checks followers_counter variable
        and functions associated with that field:
        - 'get_number_of_users_followed_by_this_user'
        - 'increment_number_of_users_followed_by_this_user'
        - 'decrement_number_of_users_followed_by_this_user'
        '''
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

    def setUp(self):
        self.test_user = User.objects.create(
            username='testuser',
            email='testuser@testcase.com',
            password='testpassword'
        )
        self.test_post = Post.objects.create(
            user=self.test_user,
            content='This is test content of test post.'
        )

    def test_post_object_was_correctly_created(self):
        '''
        Checks if post was created correctly.
        '''
        test_post = Post.objects.get(id=1)

    def test_post_object_content_variable_has_correct_value(self):
        '''
        Checks if created post's content variable has correct value.
        '''
        test_post = Post.objects.get(id=1)

        self.assertEqual(test_post.content,
                         'This is test content of test post.')

    def test_post_object_timestamp_variable_is_valid(self):
        '''
        Checks if variable timestamp is valid timestamp.
        '''
        test_post = Post.objects.get(id=1)
        timestamp = str(test_post.timestamp)

        status = False
        if re.match('\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', timestamp):
            status = True

        self.assertEqual(status, True)

    def test_post_object_serialization_method_returns_valid_json(self):
        '''
        Checks if serialize function of Post object returns valid JSON object
        '''
        test_post = Post.objects.get(id=1)

        json_response = json.dumps(str(test_post.serialize()))

        is_valid_json_status = True
        try:
            json_response = json.loads(json_response)
        except ValueError:
            is_valid_json_status = False

        self.assertEqual(is_valid_json_status, True)


class LatestPostIdViewTestCase(TestCase):
    '''
    Tests for latest_post_id_view.
    '''

    def setUp(self):
        self.test_user = User.objects.create(
            username='testuser',
            email='testuser@testcase.com',
            password='testpassword'
        )
        self.first_test_post = Post.objects.create(
            user=self.test_user,
            content='This is test content of first test post.'
        )
        self.second_test_post = Post.objects.create(
            user=self.test_user,
            content='This is test content of second test post.'
        )

    def test_latest_post_id_view_returns_correct_status_code_with_method_GET(self):
        '''
        Checks if latest_post_id_view returns
        correct http status code, when used with GET method.
        '''
        response = self.client.get(reverse('view_latest_post_id'))
        self.assertEqual(response.status_code, 200)

    def test_latest_post_id_view_returns_correct_json_object_with_method_GET(self):
        '''
        Checks if latest_post_id_view returns
        correct json object, when used with GET method.
        '''
        response = self.client.get(reverse('view_latest_post_id'))
        self.assertEqual(response.json(), {'id': 2})

    def test_latest_post_id_view_returns_json_object_with_correct_id_field_with_method_GET(self):
        '''
        Checks if latest_post_id_view returns
        correct json object, when used with GET method.
        '''
        response = self.client.get(reverse('view_latest_post_id'))
        self.assertEqual(response.json()['id'], 2)


class SinglePostViewTestCase(TestCase):
    '''
    Tests for single_post_view.
    '''

    def setUp(self):
        self.test_user = User.objects.create(
            username='testuser',
            email='testuser@testcase.com',
            password='testpassword'
        )
        self.first_test_post = Post.objects.create(
            user=self.test_user,
            content='This is test content of first test post.'
        )
        self.second_test_post = Post.objects.create(
            user=self.test_user,
            content='This is test content of second test post.'
        )

    def test_single_post_view_returns_correct_status_code_with_method_GET(self):
        '''
        Checks if single_post_view returns
        correct http status code 200, when used with GET method.
        '''
        response = self.client.get(reverse('view_single_post_by_id', args=[2]))

        self.assertEqual(response.status_code, 200)

    def test_single_post_view_returns_valid_json_object_with_method_GET(self):
        '''
        Checks if single_post_view returns
        valid json object, when used with GET method.
        '''
        response = self.client.get(reverse('view_single_post_by_id', args=[2]))

        is_valid_json_status = True

        try:
            response = json.loads(json.dumps(str(response)))
        except ValueError:
            is_valid_json_status = False

        self.assertEqual(is_valid_json_status, True)

    def test_single_post_view_returns_correct_json_object_with_method_GET(self):
        '''
        Checks if single_post_view returns
        correct json object, when used with GET method.
        '''
        first_response = self.client.get(
            reverse('view_single_post_by_id', args=[1]))
        second_response = self.client.get(
            reverse('view_single_post_by_id', args=[2]))

        self.assertEqual(first_response.json()[
                         'content'], 'This is test content of first test post.')
        self.assertEqual(second_response.json()[
                         'content'], 'This is test content of second test post.')
