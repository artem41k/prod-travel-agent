from django.test import TestCase

from django.conf import settings
from django.core.signing import Signer

from . import models


class TestAuthorization(TestCase):
    def test_403_if_unathorized(self) -> None:
        response = self.client.get('/api/trips/')
        self.assertEqual(response.status_code, 403)

    def test_403_on_profile_if_unathorized(self) -> None:
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, 403)

    def test_registration(self) -> None:
        response = self.client.post(
            '/api/profile/create/',
            {
                'tg_id': 22222222,
                'first_name': 'Testie',
                'age': 35,
                'location': 'Rome, Italy'
            }
        )
        self.assertEqual(response.status_code, 201)
        json = response.json()
        self.assertEqual(json['tg_id'], 22222222)
        self.assertNotEqual(json['location'], '')

    def test_custom_authentication(self):
        """ Test custom authentication with signed Telegram id """
        models.User.objects.create(tg_id=11111111, age=26)

        signer = Signer(key=settings.SECRET_KEY)
        auth_string = signer.sign(str(11111111))
        headers = {
            'Authentication': auth_string
        }
        response = self.client.get('/api/profile/', headers=headers)

        self.assertEqual(response.status_code, 200)
