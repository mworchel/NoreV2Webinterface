# from rest_framework.test import APIRequestFactory
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from noriv2api.models import User


class UserTest(APITestCase):

    def setUp(self):
        self.user_dict = {
                'username': 'jacob',
                'email': 'jacob@web.de',
                'password': 'top_secret'
                }
        self.user = User.objects.create_user(**self.user_dict)

    def test_get_user(self):
        self.client.force_authenticate(self.user)
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.pop('password', None), '')
        self.assertEqual(dict(response.data),
                         {'url': 'http://testserver/users/1/',
                          'username': 'jacob',
                          'email': 'jacob@web.de',
                          'user_scenes': []})

    def test_get_user_unauthenticated(self):
        url = reverse('user-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_users(self):
        self.client.force_authenticate(self.user)
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([dict(u) for u in response.data if u.pop('password', None)],
                         [{'url': 'http://testserver/users/1/',
                           'username': 'jacob',
                           'email': 'jacob@web.de',
                           'user_scenes': []}])

    def test_get_users_unauthenticated(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        user_dict = {
                'username': 'marco',
                'email': 'marco@marco.de',
                'password': 'hardhard'
                }
        url = reverse('user-list')
        response = self.client.post(url, user_dict, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.filter(username=user_dict['username']).
            first().email, user_dict['email'])

        self.assertTrue(
            User.objects.filter(username=user_dict['username']).first(). \
                                    check_password(user_dict['password']))
