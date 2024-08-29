import unittest
from unittest.mock import patch, MagicMock
from src.chatbot.chatbot import Chatbot

class TestChatbot(unittest.TestCase):

    def setUp(self):
        self.chatbot = Chatbot()
        self.chatbot.create_new_chat("test_chat")

    def test_chatbot_initialization(self):
        self.assertIsInstance(self.chatbot, Chatbot)
        self.assertEqual(len(self.chatbot.chats), 1)
        self.assertIn("gpt3", self.chatbot.models)
        self.assertIn("gpt4", self.chatbot.models)
        self.assertIn("claude", self.chatbot.models)
        self.assertIn("llama", self.chatbot.models)
        self.assertIn("custom", self.chatbot.models)

    def test_get_response_invalid_model(self):
        with self.assertRaises(ValueError):
            self.chatbot.get_response("Hello", "invalid_model", "test_chat")

    def test_get_response_invalid_chat(self):
        with self.assertRaises(ValueError):
            self.chatbot.get_response("Hello", "gpt3", "invalid_chat")

    @patch("src.chatbot.chatbot.openai.OpenAI")
    def test_gpt3_response(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Hello, I'm GPT-3!"

        self.chatbot.openai_client = mock_client
        response = self.chatbot.get_response("Hi", "gpt3", "test_chat")
        self.assertEqual(response, "Hello, I'm GPT-3!")
        mock_client.chat.completions.create.assert_called_once()

    @patch("src.chatbot.chatbot.openai.OpenAI")
    def test_gpt4_response(self, mock_openai):
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Hello, I'm GPT-4!"

        self.chatbot.openai_client = mock_client
        response = self.chatbot.get_response("Hi", "gpt4", "test_chat")
        self.assertEqual(response, "Hello, I'm GPT-4!")
        mock_client.chat.completions.create.assert_called_once()

    @patch("src.chatbot.chatbot.Anthropic")
    def test_claude_response(self, mock_anthropic):
        mock_anthropic.return_value.completions.create.return_value.completion = "Hello, I'm Claude!"
        response = self.chatbot.get_response("Hi", "claude", "test_chat")
        self.assertEqual(response, "Hello, I'm Claude!")
        mock_anthropic.return_value.completions.create.assert_called_once()

    def test_llama_response(self):
        response = self.chatbot.get_response("Hi", "llama", "test_chat")
        self.assertEqual(response, "LLaMA integration not implemented yet.")

    def test_custom_model_response(self):
        response = self.chatbot.get_response("Hi", "custom", "test_chat")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_get_chat_history(self):
        self.chatbot.get_response("Hello", "gpt3", "test_chat")
        self.chatbot.get_response("How are you?", "gpt3", "test_chat")
        history = self.chatbot.get_chat_history("test_chat")
        self.assertEqual(len(history), 4)  # 2 user messages + 2 AI responses
        self.assertTrue(history[0].startswith("Human: Hello"))
        self.assertTrue(history[2].startswith("Human: How are you?"))

    def test_clear_chat_history(self):
        self.chatbot.get_response("Hello", "gpt3", "test_chat")
        self.chatbot.clear_chat_history("test_chat")
        history = self.chatbot.get_chat_history("test_chat")
        self.assertEqual(len(history), 0)

    def test_list_chats(self):
        self.chatbot.create_new_chat("chat2")
        chats = self.chatbot.list_chats()
        self.assertIn("test_chat", chats)
        self.assertIn("chat2", chats)

    def test_delete_chat(self):
        self.chatbot.create_new_chat("chat_to_delete")
        self.chatbot.delete_chat("chat_to_delete")
        chats = self.chatbot.list_chats()
        self.assertNotIn("chat_to_delete", chats)

if __name__ == "__main__":
    unittest.main()
