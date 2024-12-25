from flask import request, jsonify
from app.auth.routes import auth_bp


@auth_bp.route("/protected", methods=["GET"])
@token_required
def protected(payload):
        return jsonify({"message": "Success", "user": payload})