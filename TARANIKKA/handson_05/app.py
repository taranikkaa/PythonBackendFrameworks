# app.py
from flask import Flask, jsonify
from config import Config
from coursemanager.extensions import db, migrate
from coursemanager.routes import courses_bp
from coursemanager import models 

def create_app():  # <--- MAKE SURE THIS IS SPELLED EXACTLY LIKE THIS
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(courses_bp)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'status': 'error', 'message': 'An internal server error occurred'}), 500

    return app

if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5000)