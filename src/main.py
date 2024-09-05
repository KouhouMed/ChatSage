import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .chatbot.chatbot import Chatbot
from .config import Config
from .web.routes import bp as main_bp
from .models import db, User


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "web", "templates")
        ),
        static_folder=os.path.abspath(
            os.path.join(os.path.dirname(__file__), "web", "static")
        ),
    )
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "main.login"
    bcrypt = Bcrypt(app)

    # Initialize chatbot
    app.chatbot = Chatbot()

    # Register blueprints
    app.register_blueprint(main_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app


def main():
    app = create_app()

    @app.route("/api/chat", methods=["POST"])
    def chat():
        data = request.json
        user_message = data.get("message")
        model = data.get("model", "gpt3")  # Default to GPT-3 if not specified
        chat_id = data.get("chat_id")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        try:
            response = app.chatbot.get_response(user_message, model, chat_id)
            return jsonify({"response": response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Create database tables
    with app.app_context():
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()
