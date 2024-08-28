import os
from flask import Flask, request, jsonify
from src.chatbot.chatbot import Chatbot
from src.config import Config
from src.web.routes import configure_routes


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize chatbot
    app.chatbot = Chatbot()

    # Configure routes
    configure_routes(app)

    return app


def main():
    app = create_app()

    @app.route('/api/chat', methods=['POST'])
    def chat():
        data = request.json
        user_message = data.get('message')
        model = data.get('model', 'gpt3')  # Default to GPT-3 if not specified

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        try:
            response = app.chatbot.get_response(user_message, model)
            return jsonify({'response': response})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()
