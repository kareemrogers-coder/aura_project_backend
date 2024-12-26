from flask import request, jsonify
from auth import auth_bp
from utils.util import token_required


@auth_bp.route("/protected", methods=["GET"])
@token_required
def protected(payload):
        return jsonify({"message": "Success", "user": payload})