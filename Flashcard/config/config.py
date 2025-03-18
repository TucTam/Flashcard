import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', "fallback-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', "sqlite:///default.db")
    
    # Use __file__ to get the current file path and work from there
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    TEMPLATE_FOLDER = os.path.join(BASE_DIR, "app/templates")
    STATIC_FOLDER = os.path.join(BASE_DIR, "app/static")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_IMAGE_MIME_TYPES = {"image/jpeg", "image/png", "image/webp"}  # Moved here

class DevelopmentConfig(Config):
    """Development-specific settings"""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Logs SQL queries (for debugging)
    
class ProductionConfig(Config):
    """Production-specific settings"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Use production DB
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class TestingConfig(Config):
    """Testing-specific settings"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing