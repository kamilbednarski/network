from django.test import TestCase
from network.models import User, Post, Like, Relation


class UserTestCase(TestCase):
    '''
    Tests for User model.
    '''
    def set_up_new_test_user(self):
        first_test_user = User.objects.create(
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


    def test_users_fields_have_correct_values(self):
        '''
        Checks if created users' fields have correct values.
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