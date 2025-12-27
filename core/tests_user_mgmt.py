from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class UserManagementTests(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.admin_user = self.User.objects.create_superuser(
            username='admin',
            password='password',
            job_number='ADMIN001'
        )
        self.client = Client()
        self.client.login(username='admin', password='password')

    def test_user_list_view(self):
        response = self.client.get(reverse('user_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'إدارة المستخدمين')

    def test_user_create_view(self):
        url = reverse('user_create')
        data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'job_number': '12345',
            'mobile_number': '0500000000',
            'password': 'StrongPass123!@#',
            'rank': 'CIV',
            'role': 'ANALYST'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('user_list'))
        
        # Verify user created
        new_user = self.User.objects.get(username='newuser')
        self.assertEqual(new_user.mobile_number, '0500000000')
        self.assertEqual(new_user.job_number, '12345')
        self.assertTrue(new_user.check_password('StrongPass123!@#'))
        
        # Verify QR code generated
        self.assertTrue(new_user.qr_code)

    def test_user_search(self):
        # Create user to search
        self.User.objects.create_user(
            username='searchtarget',
            job_number='99999',
            mobile_number='0599999999'
        )
        
        response = self.client.get(reverse('user_list'), {'q': '99999'})
        self.assertContains(response, 'searchtarget')
        
        response = self.client.get(reverse('user_list'), {'q': '0599999999'})
        self.assertContains(response, 'searchtarget')

    def test_qr_login_with_new_user(self):
        # Create user
        user = self.User.objects.create_user(username='qruser', password='pw')
        # Simulate QR scan data
        qr_data = f"USER:qruser|JOB:None|UID:{user.id}"
        
        response = self.client.post(
            reverse('qr_login'),
            data={'qr_data': qr_data},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])

    def test_user_create_with_national_id(self):
        url = reverse('user_create')
        data = {
            'username': 'natuser',
            'first_name': 'Nat',
            'last_name': 'User',
            'email': 'nat@example.com',
            'job_number': '54321',
            'national_id': '1000000001',
            'mobile_number': '0555555555',
            'password': 'StrongPass123!@#',
            'rank': 'CIV',
            'role': 'ANALYST'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('user_list'))
        
        # Verify user created with national_id
        new_user = self.User.objects.get(username='natuser')
        self.assertEqual(new_user.national_id, '1000000001')
        self.assertEqual(new_user.email, 'nat@example.com')

    def test_password_recovery_with_national_id(self):
        # Create user with national_id
        user = self.User.objects.create_user(
            username='recoveruser',
            email='recover@example.com',
            password='oldpassword',
            job_number='REC001',
            national_id='1000000002'
        )
        
        url = reverse('password_reset_request') # Ensure this URL name matches urls.py
        data = {
            'job_number': 'REC001',
            'national_id': '1000000002',
            'email': 'recover@example.com',
            'new_password': 'NewStrongPassword123!'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "تم تغيير كلمة المرور بنجاح")
        
        # Verify password changed
        user.refresh_from_db()
        self.assertTrue(user.check_password('NewStrongPassword123!'))
