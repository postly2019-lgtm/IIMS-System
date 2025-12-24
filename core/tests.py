from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

class SystemTest(TestCase):
    def test_sec_user_card(self):
        User = get_user_model()
        # Create sec user
        user = User.objects.create_superuser(
            username='sec',
            password='Aa159632@',
            job_number='SEC-001',
            rank='MIL',
            first_name='مدير',
            last_name='النظام'
        )
        
        # Check if QR code is generated automatically
        self.assertTrue(user.qr_code)
        print(f"\n[TEST] QR Code Path: {user.qr_code.name}")
        
        # Check Card View
        url = reverse('user_card', args=[user.username])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # Check for Arabic content and fields
        self.assertContains(response, 'SEC-001')
        self.assertContains(response, 'عسكري') # Rank Display
        self.assertContains(response, 'مدير النظام') # Full Name
        
        print("\n[TEST] Card View validated successfully.")
