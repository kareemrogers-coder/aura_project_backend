from flask import Flask, request, jsonify, redirect, url_for, Request
from PIL import Image
from app.models import Users, Images, db 
from .schemas import image_schema, images_schema
from werkzeug.utils import secure_filename
from app.blueprints.images import images_bp
from io import BytesIO
from urllib.parse import urljoin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import os
from flask_login import current_user

# check if the dir call "uplaods" exists
upload_folder = os.path.join(os.getcwd(), 'uploads')
allowed_extension ={"png", "jpg", "jpeg","gif"}

#id the dir doesnt exist then create it.
if not os.path.exists(upload_folder):
    os.markdirs(upload_folder)

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in allowed_extension

###this route is used to upload images as url
@images_bp.route('/upload', methods=['POST'])
def image_upload():
    if 'image' not in Request.files:
        return jsonify ({"error": "No file part"}), 400
    
    file = Request.files['image']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        if not current_user.is_authenticated:
            return jsonify({"error": "User no authenticated"}), 401
        
        filename = secure_filename(file.filename)

        # save the url file locally
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        image_url = urljoin(Request.host_url, os.path.realpath(file_path, os.getcwd()))

        # save and create new iamge record in the database
        new_image = Images(image_url=image_url, user_id=current_user.id)

        # add to db 
        db.session.add(new_image)
        db.session.commit()

        return jsonify({
            "message": "Image uploaded successfully",
            "image_id": new_image.id,
            "image_url": new_image.image_url
        }), 201
    
    return jsonify ({"error": "Invaild file format"}), 400


### this route was used to upload images as binary number 
# @images_bp.route('/upload', methods=['POST'])
# def image_upload():
#     if 'image' not in request.files:
#         return jsonify ({"error": "No file part" }), 400
    

#     file = request.files['image']


#     if file.filename == '':
#         return jsonify ({"error": "No selected file"}), 400
    
#     if file and allowed_file(file.filename):

#         if not current_user.is_authenticated:
#             return jsonify({"error": "User not authenticated"}), 401

#         # user_id = request.form.get('user_id')

#         filename = secure_filename(file.filename)

#         img = Image.open(file.stream)
#         img_byte_arr = BytesIO()
#         img.save(img_byte_arr, format = 'PNG')
#         img_byte_arr.seek(0)

#         new_image = Images(image=img_byte_arr.read(), user_id = current_user.id)

#         db.session.add(new_image)
#         db.session.commit()

#         return jsonify({ "messages": "Images uploaded successfully", "images_id": new_image.id}), 201
    
#     return jsonify({"error": "Invalid file format"}), 400





### retrieve all images based on the user that is logged in####
@images_bp.route('/users_images/<int:user_id>', methods=['Get'])
def get_user_images(user_id):

    images = Images.query.filter_by(user_id=user_id).all()
    if not images:
        return jsonify({"error": "No Images are currently store for this user"}), 404
    
    image_list = [{"images_id": img.id, "image_url": img.image_url} for img in images]

    return jsonify({ "user_id": user_id, "images": image_list}), 200



### retrieve all images regardless of the user####
@images_bp.route("/", methods=["GET"])
def get_images():
    query = select(Images)
    images = db.session.execute(query).scalars().all()

    image_list = [{ "image_id": img.id, "image_url": img.image_url} for img in images]

    return jsonify({"images": image_list}), 200