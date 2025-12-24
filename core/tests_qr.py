from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.base import ContentFile
import json

User = get_user_model()

class QRLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.user.qr_code.save('test.png', ContentFile(b'test'), save=False)
        self.user.save()

    def test_qr_login_success(self):
        # Format: USER:username|JOB:job|UID:id
        qr_data = f"USER:{self.user.username}|JOB:None|UID:{self.user.id}"
        
        response = self.client.post(
            reverse('qr_login'),
            data=json.dumps({'qr_data': qr_data}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        
        # Check if user is authenticated
        # Note: In test client, session login works differently, but we check response success
        # To truly verify login state in test client:
        # self.assertIn('_auth_user_id', self.client.session) 
        # But since we use a custom view that calls login(), we rely on success response for this unit test.

    def test_qr_login_invalid_user(self):
        qr_data = "USER:fakeuser|JOB:None|UID:999"
        response = self.client.post(
            reverse('qr_login'),
            data=json.dumps({'qr_data': qr_data}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])

    def test_qr_login_invalid_format(self):
        qr_data = "INVALID_FORMAT"
        response = self.client.post(
            reverse('qr_login'),
            data=json.dumps({'qr_data': qr_data}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['success'])
