# app.py
from flask import Flask, jsonify
from config import Config
from coursemanager.routes import courses_bp

def create_app():
    # Step 37: Application factory pattern
    app = Flask(__name__)
    
    # Step 38: Load configuration
    app.config.from_object(Config)
    
    # Step 40: Register the blueprint
    app.register_blueprint(courses_bp)
    
    # Step 45: Global Error Handlers returning JSON instead of HTML
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'An internal server error occurred'
        }), 500

    return app

# Allow running the app directly via: python app.py
if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5000)