from flask import Blueprint, jsonify, request, render_template, current_app
from flask_cors import cross_origin
from functools import wraps
import time

# Create a Blueprint for our routes
bp = Blueprint('main', __name__)


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


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/api/chat', methods=['POST'])
@cross_origin()
@rate_limit(10)  # Limit to 10 requests per minute
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400

    message = data['message']
    model = data.get('model', current_app.config['DEFAULT_MODEL'])

    try:
        response = current_app.chatbot.get_response(message, model)
        return jsonify({"response": response})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        current_app.logger.error(f"Error processing chat request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@bp.route('/api/models', methods=['GET'])
def get_models():
    return jsonify({"models": list(current_app.chatbot.models.keys())})


@bp.route('/api/history', methods=['GET'])
def get_history():
    history = current_app.chatbot.get_chat_history()
    return jsonify({"history": history})


@bp.route('/api/clear_history', methods=['POST'])
def clear_history():
    current_app.chatbot.history.clear()
    return jsonify({"message": "Chat history cleared"})


@bp.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@bp.errorhandler(500)
def internal_error(error):
    current_app.logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


def configure_routes(app):
    app.register_blueprint(bp)