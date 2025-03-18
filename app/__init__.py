from flask import Flask, Blueprint
from config.config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from .database import db
from flask_migrate import Migrate
import os

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder=Config.STATIC_FOLDER)
    
    
    app.config.from_object(Config)
    
    # Get the environment (default to development)
    env = os.getenv("FLASK_ENV", "development")

    # Select the config based on the environment
    if env == "production":
        app.config.from_object(ProductionConfig)
    elif env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)  # Default to development
   
    db.init_app(app)
    
    migrate = Migrate(app, db)
    
    # Blueprint routes
    from .modules.Main import main as main_blueprint
    from .modules.Flashcards.Create import create as create_blueprint
    from .modules.Flashcards.Manage import manage as manage_blueprint
    from .modules.Flashcards.Study import study as study_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(study_blueprint, url_prefix='/Flashcards/study')
    app.register_blueprint(create_blueprint, url_prefix='/Flashcards/create')
    app.register_blueprint(manage_blueprint, url_prefix='/Flashcards/manage')

        
    return app