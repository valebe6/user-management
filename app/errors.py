from flask import jsonify
from marshmallow import ValidationError
from pymongo.errors import DuplicateKeyError

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation(err):
        return jsonify({
            "error": "validation_error",
            "messages": err.messages
        }), 400

    @app.errorhandler(DuplicateKeyError)
    def handle_duplicate(err):
        return jsonify({
            "error": "duplicate_error",
            "message": "Resource already exists"
        }), 409

    @app.errorhandler(404)
    def not_found(err):
        return jsonify({
            "error": "not_found",
            "message": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def server_error(err):
        return jsonify({
            "error": "internal_server_error",
            "message": "Unexpected error"
        }), 500
