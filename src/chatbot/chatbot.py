import os
import openai
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Chatbot:
    def __init__(self):
        self.models = {
            "gpt3": self.gpt3_response,
            "gpt4": self.gpt4_response,
            "claude": self.claude_response,
            "llama": self.llama_response,
            "custom": self.custom_model_response,
        }
        self.chats = {"default": []}  # Initialize with a default chat

        # Initialize custom model (example with a small GPT-2 model)
        self.custom_tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.custom_model = AutoModelForCausalLM.from_pretrained("gpt2")

        # Initialize OpenAI client if API key is available
        self.openai_client = None
        if os.getenv("OPENAI_API_KEY"):
            self.openai_client = openai.OpenAI()

        # Initialize Anthropic client if API key is available
        self.anthropic_client = None
        if os.getenv("ANTHROPIC_API_KEY"):
            self.anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def get_response(self, message, model="gpt3", chat_id="default"):
        if model not in self.models:
            raise ValueError(f"Model {model} not supported")

        if chat_id not in self.chats:
            self.chats[chat_id] = []

        self.chats[chat_id].append(f"Human: {message}")
        response = self.models[model](message)
        self.chats[chat_id].append(f"AI: {response}")

        return response

    def gpt3_response(self, message):
        if not self.openai_client:
            return "OpenAI API key not set. Unable to use GPT-3."
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo", messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in GPT-3 response: {str(e)}"

    def gpt4_response(self, message):
        if not self.openai_client:
            return "OpenAI API key not set. Unable to use GPT-4."
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4", messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error in GPT-4 response: {str(e)}"

    def claude_response(self, message):
        if not self.anthropic_client:
            return "Anthropic API key not set. Unable to use Claude."
        try:
            response = self.anthropic_client.completions.create(
                model="claude-2",
                prompt=f"{HUMAN_PROMPT} {message} {AI_PROMPT}",
                max_tokens_to_sample=300,
            )
            return response.completion
        except Exception as e:
            return f"Error in Claude response: {str(e)}"

    def llama_response(self, message):
        # Placeholder for LLaMA integration
        return "LLaMA integration not implemented yet."

    def custom_model_response(self, message):
        try:
            input_ids = self.custom_tokenizer.encode(message, return_tensors="pt")
            attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

            with torch.no_grad():
                output = self.custom_model.generate(
                    input_ids,
                    attention_mask=attention_mask,
                    max_length=100,
                    num_return_sequences=1,
                    no_repeat_ngram_size=2,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.95,
                )

            response = self.custom_tokenizer.decode(
                output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True
            )
            return response
        except Exception as e:
            return f"Error in custom model response: {str(e)}"

    def get_chat_history(self, chat_id="default"):
        return self.chats.get(chat_id, [])

    def get_all_chats(self):
        return {chat_id: {"name": f"Chat {chat_id}", "messages": messages} for chat_id, messages in self.chats.items()}

    def clear_chat_history(self, chat_id="default"):
        if chat_id in self.chats:
            self.chats[chat_id] = []
        else:
            raise ValueError(f"Chat {chat_id} not found")
