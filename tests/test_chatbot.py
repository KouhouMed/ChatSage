import unittest
from unittest.mock import patch
from src.chatbot.chatbot import Chatbot


class TestChatbot(unittest.TestCase):

    def setUp(self):
        self.chatbot = Chatbot()

    def test_chatbot_initialization(self):
        self.assertIsInstance(self.chatbot, Chatbot)
        self.assertEqual(len(self.chatbot.history), 0)
        self.assertIn('gpt3', self.chatbot.models)
        self.assertIn('gpt4', self.chatbot.models)
        self.assertIn('claude', self.chatbot.models)
        self.assertIn('llama', self.chatbot.models)
        self.assertIn('custom', self.chatbot.models)

    def test_get_response_invalid_model(self):
        with self.assertRaises(ValueError):
            self.chatbot.get_response("Hello", "invalid_model")

    @patch('src.chatbot.chatbot.openai.ChatCompletion.create')
    def test_gpt3_response(self, mock_create):
        mock_create.return_value.choices[0].message.content = "Hello, I'm GPT-3!"
        response = self.chatbot.gpt3_response("Hi")
        self.assertEqual(response, "Hello, I'm GPT-3!")
        mock_create.assert_called_once()

    @patch('src.chatbot.chatbot.openai.ChatCompletion.create')
    def test_gpt4_response(self, mock_create):
        mock_create.return_value.choices[0].message.content = "Hello, I'm GPT-4!"
        response = self.chatbot.gpt4_response("Hi")
        self.assertEqual(response, "Hello, I'm GPT-4!")
        mock_create.assert_called_once()

    @patch('src.chatbot.chatbot.Anthropic')
    def test_claude_response(self, mock_anthropic):
        mock_anthropic.return_value.completions.create.return_value.completion = "Hello, I'm Claude!"
        response = self.chatbot.claude_response("Hi")
        self.assertEqual(response, "Hello, I'm Claude!")
        mock_anthropic.return_value.completions.create.assert_called_once()

    def test_llama_response(self):
        response = self.chatbot.llama_response("Hi")
        self.assertEqual(response, "LLaMA integration not implemented yet.")

    def test_custom_model_response(self):
        response = self.chatbot.custom_model_response("Hi")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_get_chat_history(self):
        self.chatbot.get_response("Hello", "gpt3")
        self.chatbot.get_response("How are you?", "gpt3")
        history = self.chatbot.get_chat_history()
        self.assertEqual(len(history), 4)  # 2 user messages + 2 AI responses
        self.assertTrue(history[0].startswith("Human: Hello"))
        self.assertTrue(history[2].startswith("Human: How are you?"))


if __name__ == '__main__':
    unittest.main()
