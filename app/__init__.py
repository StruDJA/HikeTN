from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .site.routes import site
from .api.routes import api
from .api.models import setup_db

def create_app():
  app = Flask(__name__)
  CORS(app)
  app.register_blueprint(site)
  app.register_blueprint(api)
  setup_db(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response
  
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success': False,
          'error': 404,
          'message': 'Not found'
      }), 404

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
          'success': False,
          'error': 500,
          'message': 'Internal server error'
      }), 500

  return app