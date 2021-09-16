from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config=Config):
	app = Flask(__name__)
	app.config.from_object(config)
	db.init_app(app)
	migrate.init_app(app, db)
	cors.init_app(app)

	from .blueprints.api import bp as api_bp
	app.register_blueprint(api_bp)

	return app