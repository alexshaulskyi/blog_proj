from django.test import TestCase, Client
from django.core import mail

from posts.models import User


class EmailTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('dummy_two', 'dummy_two@dummy_two.com', 'dummy_two')

    def test_profile_page_code(self):
        """ Tests if profile page is accessible """
        response = self.client.get('/dummy_two/')
        self.assertEqual(response.status_code, 200)
 
    def test_send_msg(self):
        """Tests if an email is being sent to a user upon registration completion"""
        mail.send_mail(
            'Successful registration', 'Sup, welcome to Yatubah', 'yatube@yatube.com', ['{{self.user.email}}'], fail_silently=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Successful registration')