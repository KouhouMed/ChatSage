# ChatSage


![ChatSage CI](https://github.com/KouhouMed/chatsage/workflows/ChatSage%20CI/badge.svg)
[![codecov](https://codecov.io/gh/KouhouMed/chatsage/branch/main/graph/badge.svg)](https://codecov.io/gh/KouhouMed/chatsage)

ChatSage is a multi-model chatbot application that allows users to interact with various language models including GPT-3, GPT-4, Claude, and custom models.

## Features

- Support for multiple language models (GPT-3, GPT-4, Claude, LLaMA, and custom models)
- Web-based chat interface
- API endpoints for chat functionality
- Configurable settings for different environments
- Basic rate limiting
- Chat history management

![ChatSage UI](https://kouhoumed.com/chatsage-ui.png)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/KouhouMed/ChatSage
   cd ChatSage
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the package and its dependencies:
   ```
   pip install -e .
   ```

4. Create a `.env` file in the project root and add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

## Usage

1. Run the application:
   ```
   python run.py
   ```

2. Open a web browser and navigate to `http://localhost:5000` to access the chat interface.

3. Select a model from the dropdown menu, type your message, and click "Send" to chat with the selected model.

## API Endpoints

- `POST /api/chat`: Send a chat message
  - Request body: `{"message": "Your message", "model": "gpt3"}`
  - Response: `{"response": "Model's response"}`

- `GET /api/models`: Get available models
  - Response: `{"models": ["gpt3", "gpt4", "claude", "llama", "custom"]}`

- `GET /api/history`: Get chat history
  - Response: `{"history": ["Human: Hello", "AI: Hi there!"]}`

- `POST /api/clear_history`: Clear chat history
  - Response: `{"message": "Chat history cleared"}`

## Development

To install development dependencies:
```
pip install -e .[dev]
```

To run tests:
```
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.