from flask import Flask, request, jsonify, redirect, url_for
from PIL import Image
from app.models import Users, Images, db 
from .schemas import image_schema, images_schema
from werkzeug.utils import secure_filename
from app.blueprints.images import images_bp
from io import BytesIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in {"png", "jpg", "jpeg", "gif"} 

@images_bp.route('/upload', methods=['POST'])
def image_upload():
    if 'image' not in request.files:
        return jsonify ({"error": "No file part" }), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify ({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):

        user_id = request.form.get('user_id')

        filename = secure_filename(file.filename)

        img = Image.open(file.stream)
        img_byte_arr = BytesIO
        img.save(img_byte_arr, formate = 'PNG')
        img_byte_arr.seek(0)

        new_image = Images(image=img_byte_arr.read(), user_id=user_id)

        db.session.add(new_image)
        db.session.commit()

        return jsonify({ "messages": "Images uploaded successfully", "images_id": new_image.id}), 201
    
    return jsonify({"error": "Invalid file formate"}), 400


@images_bp.route('/users_images/<int:user_id>', methods=['Get'])
def get_user_images(user_id):

    images = Images.query.filter_by(user_id=user_id).all()
    image_list = [{"images_id": img.id} for img in images]
    return jsonify({ "user_id": user_id, "images": image_list}), 200


@images_bp.route("/", methods=["GET"])
def get_images():
    query = select(Images)
    users = db.session.execute(query).scalars().all()

    return images_schema.jsonify(users), 200