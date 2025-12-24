from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from core.models import UserActionLog
from intelligence.models import IntelligenceReport, Source
from django.urls import reverse

User = get_user_model()

class AuditLogTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='analyst', password='password')
        self.client.login(username='analyst', password='password')
        
        self.source = Source.objects.create(name="News Agency", source_type="RSS", reliability_score=80)
        self.report = IntelligenceReport.objects.create(
            title="Secret Report",
            content="Content",
            source=self.source,
            classification="SECRET"
        )

    def test_view_report_creates_log(self):
        url = reverse('report_detail', args=[self.report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Check log
        log = UserActionLog.objects.last()
        self.assertIsNotNone(log)
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.action, UserActionLog.ActionType.VIEW_REPORT)
        self.assertIn(str(self.report.id), log.target_object)

    def test_search_creates_log(self):
        url = reverse('search') + '?q=secret'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        # Check log
        log = UserActionLog.objects.filter(action=UserActionLog.ActionType.SEARCH).last()
        self.assertIsNotNone(log)
        self.assertEqual(log.user, self.user)
        self.assertIn("secret", log.target_object)

    def test_audit_view_access(self):
        # Ordinary user should not access
        url = reverse('audit_log')
        response = self.client.get(url)
        # Expect redirect to login (next=/audit/) because user_passes_test redirects on failure by default
        self.assertEqual(response.status_code, 302) 

        # Staff user should access
        self.user.is_staff = True
        self.user.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
