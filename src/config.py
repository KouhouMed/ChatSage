import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # Flask settings
    SECRET_KEY = os.getenv("SECRET_KEY") or "you-will-never-guess"
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

    # Model settings
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt3")

    # Custom model path (if using a local model)
    CUSTOM_MODEL_PATH = os.getenv("CUSTOM_MODEL_PATH", "models/custom_model")

    # Database settings (if you decide to use a database later)
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///chatsage.db")

    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Rate limiting
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100/day")

    # Maximum conversation history to maintain
    MAX_HISTORY = int(os.getenv("MAX_HISTORY", 50))

    @staticmethod
    def init_app(app):
        # You can perform any necessary initialization here
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True


# Dictionary to easily switch between configurations
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}

# Set the active configuration
active_config = config[os.getenv("FLASK_ENV", "default")]
