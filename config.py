from flask import app
import os

#Config
class Config():
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'testkey'
	SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
	SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')