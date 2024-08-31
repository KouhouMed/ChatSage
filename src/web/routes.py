from flask import Blueprint, jsonify, request, render_template, current_app
from flask_cors import cross_origin
from functools import wraps
import time

bp = Blueprint("main", __name__)


def rate_limit(limit_per_minute):

    def decorator(f):
        last_request_time = {}
        @wraps(f)
        def wrapped(*args, **kwargs):
            now = time.time()
            if request.remote_addr in last_request_time:
                time_passed = now - last_request_time[request.remote_addr]
                if time_passed < 60 / limit_per_minute:
                    return jsonify({"error": "Rate limit exceeded"}), 429
            last_request_time[request.remote_addr] = now
            return f(*args, **kwargs)
        return wrapped
    return decorator


@bp.route("/about")
def about():
    return render_template("about.html")


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/api/chat", methods=["POST"])
@cross_origin()
@rate_limit(10)  # Limit to 10 requests per minute
def chat():
    data = request.json
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    message = data["message"]
    model = data.get("model", current_app.config["DEFAULT_MODEL"])
    chat_id = data.get("chat_id", "default")

    try:
        response = current_app.chatbot.get_response(message, model, chat_id)
        return jsonify({"response": response})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route("/api/history", methods=["GET"])
def get_history():
    chats = current_app.chatbot.get_all_chats()
    return jsonify({"chats": chats})


@bp.route("/api/clear_history", methods=["POST"])
def clear_history():
    data = request.json
    chat_id = data.get("chat_id", "default") if data else "default"
    try:
        current_app.chatbot.clear_chat_history(chat_id)
        return jsonify({"message": f"Chat history cleared for chat {chat_id}"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@bp.errorhandler(500)
def internal_error(error):
    current_app.logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


def configure_routes(app):
    app.register_blueprint(bp)
