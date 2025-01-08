from flask import Blueprint, request, jsonify
from PIL import Image
from io import BytesIO
from werkzeug.utils import secure_filename
from flask_login import current_user
from app.models import db, Leaderboard, Images, LeaderboardComment, LeaderboardLike
from app.blueprints.leaderboard import leaderboard_bp

def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in {"png", "jpg", "jpeg", "gif"} 

@leaderboard_bp.route('/upload', methods=['POST'])
def upload_leaderboard_image():
    if 'image' not in request.files:
        return jsonify({"error": "No file Part"}), 400
    file = request.files['images']
    if file.filename == '':
        return jsonify ({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        img = Image.open(file.stream)
        img_byte_arr = BytesIO
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        leaderboard_image = Leaderboard(
            image = img_byte_arr.read(),
            user_id = current_user.id
        )

        try:
            db.session.add(leaderboard_image)
            db.session.commit()
            return jsonify({
                "message": "Image uploaded successfully to the leaderboard", "image id": leaderboard_image.id
            }), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Image upload unsuccessful"}), 500
    return jsonify({"error": "Invalid file format"}), 400


@leaderboard_bp.route('/comment', methods= ['POST'])
def add_comment():
    text = request.form.get("text")
    leaderboard_image_id = request.form.get("leaderboard_image_id")

    if not text or not leaderboard_image_id: 
        return jsonify({"error": "no text found"}), 400
    
    try:
        leaderboard_image = Leaderboard.query.get(leaderboard_image_id)
        if not leaderboard_image:
            return jsonify({"error": "image does not exist"}), 404
        
        comment = LeaderboardComment(
            text = text,
            user_id = current_user.id,
            leaderboard_image_id = leaderboard_image.id
        )

        db.session.add(comment)
        db.session.commit

        return jsonify({ "message": "Comment has been added successfully", "comment_id": comment.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "comment wasn't added, please try again"}), 500
    


@leaderboard_bp.route('/like', methods = ['POST'])
def like_image():
    leaderboard_image_id = request.form.get('leaderboard_image_id')

    if not leaderboard_image_id:
        return jsonify({"error": "No more Leaderboard image id found."})
    
    try:
        leaderboard_image = Leaderboard.query.get(leaderboard_image_id)
        if not leaderboard_image:
            return jsonify({"error": "Image not found"})
        
        exist_like = LeaderboardLike.query.filter_by(
            user_id = current_user.id,
            leaderboard_image_id = leaderboard_image.id
        ).first()

        if exist_like:
            return jsonify({"error": "Only one like allowed, you have liked this image"}), 400
        
        like = LeaderboardLike(
            user_id = current_user.id,
            leaderboard_image_id = leaderboard_image.id
            )


        db.session.add(like)
        db.session.commit


        return jsonify({
            "message": "Imaged Liked",
            "like_count": leaderboard_image.like_count()

        }), 201


    except Exception as e:
        db.session.rollback()
        return jsonify ({"error": "Like wasnt accounted for, Please try again."}), 500