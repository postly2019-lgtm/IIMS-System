from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
from .models import AgentSession, AgentMessage, AgentInstruction

User = get_user_model()

class IntelligenceAgentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='agent_user',
            password='password123',
            role=User.Role.ADMIN,
            is_staff=True,
            is_superuser=True,
        )
        self.client.force_login(self.user)

    def test_agent_chat_view_loads(self):
        """Test that the chat page loads correctly."""
        response = self.client.get(reverse('agent_chat_root'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'intelligence_agent/chat.html')

    def test_create_new_session(self):
        """Test creating a new chat session."""
        response = self.client.get(reverse('agent_new_session'))
        self.assertEqual(response.status_code, 302) # Redirects to chat
        self.assertTrue(AgentSession.objects.filter(user=self.user).exists())

    @patch('intelligence_agent.views.GroqClient')
    def test_send_message_flow(self, MockGroqClient):
        """Test sending a message and receiving a mock response."""
        # Setup Mock
        mock_instance = MockGroqClient.return_value
        mock_instance.chat_completion.return_value = "This is a mocked AI response."

        # 1. Create Session
        session = AgentSession.objects.create(user=self.user, title="Test Session")
        
        # 2. Send Message
        url = reverse('agent_send_message', args=[session.id])
        data = {'content': 'Analyze this threat'}
        response = self.client.post(url, data)
        
        # 3. Verify Response
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['status'], 'success')
        self.assertEqual(json_response['ai_message'], "This is a mocked AI response.")
        
        # 4. Verify DB
        self.assertEqual(AgentMessage.objects.filter(session=session).count(), 2) # User + Assistant

    def test_settings_update(self):
        """Test updating the system prompt."""
        url = reverse('agent_settings')
        new_prompt = "You are a strict military analyst."
        
        data = {
            'update_instruction': '1',
            'system_prompt': new_prompt
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        
        instruction = AgentInstruction.objects.first()
        self.assertEqual(instruction.system_prompt, new_prompt)
