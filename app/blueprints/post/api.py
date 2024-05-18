from flask import request, jsonify, session, current_app
import os
from werkzeug.utils import secure_filename
from . import post_api_bp, post_helper
from db import db_error_helper as ERROR
from app.blueprints.puzzle import puzzle_helper
from app.blueprints.comment import comment_helper
from app.blueprints.user.user_helper import user_service


def allowed_file(filename, ALLOWED_EXT=['jpg', 'jpeg', 'png', 'gif']):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT


@post_api_bp.route('/api/getpost', methods=['POST'])
def get_post():
    data = request.get_json()
    try:
        post = post_helper.get_post(data)
        puzzledata = puzzle_helper.get_puzzle({"puzzleid": post['puzzleid']})
        comment = comment_helper.get_comments({"postid": data['postid']})
        if comment is not None:
            for item in comment:
                item['author'] = user_service.get_username(item['userid'])
                item.pop('userid')
        return jsonify({"postid": post['postid'], "title": post['title'], "content": post['content'],
                        "puzzledata": puzzledata, "comments": comment}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error getting post: {e}"}), 401


@post_api_bp.route('/api/addpost', methods=['POST'])
def add_post():
    data = request.form.to_dict()
    data['userid'] = session.get('userid')
    if not data['userid']:
        return jsonify({"message": "Please login before creating a post"}), 401

    try:
        generated_story = post_helper.generate_story(data['title'], data['content'], data['characters'], data['answer'])
        puzzle_data = {
            'userid': data['userid'],
            'puzzledata': generated_story,
            'category': '',
            'puzzleanswer': data['answer']
        }
        puzzle_id = puzzle_helper.add_puzzle(puzzle_data)
        data['puzzleid'] = puzzle_id
        postid = post_helper.add_post(data)

        isupload = False
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"message": "Filename is blank or corrupted."}), 401
            if file and allowed_file(file.filename):
                for existing_file in os.listdir(current_app.config['UPLOAD_FOLDER']):
                    existing_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], existing_file)
                    if os.path.isfile(existing_file_path) and existing_file.startswith(str(postid) + '.'):
                        os.remove(existing_file_path)
                filename = str(postid) + os.path.splitext(secure_filename(file.filename))[1]
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                post_helper.add_image({"postid": postid, "postimage": filename})
                isupload = True
            else:
                return jsonify({"message": "Invalid file type"}), 401

        if isupload:
            return jsonify({"message": "Post added successfully with image", "newpostid": postid,
                            "story": generated_story, "postid": postid}), 200
        else:
            return jsonify({"message": "Post added successfully. No image found.", "newpostid": postid,
                            "story": generated_story, "postid": postid}), 200
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error adding post: {e}"}), 401
    except RuntimeError as e:
        return jsonify({"message": f"Error adding post: {e}"}), 401



@post_api_bp.route('/api/uploadimage/<int:postid>', methods=['POST'])
def upload_image(postid):
    try:
        if 'file' not in request.files:
            return jsonify({"message": "No file part"}), 401
        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "No selected file"}), 401
        if file and allowed_file(file.filename):
            for existing_file in os.listdir(current_app.config['UPLOAD_FOLDER']):
                existing_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], existing_file)
                if os.path.isfile(existing_file_path) and existing_file.startswith(str(postid) + '.'):
                    os.remove(existing_file_path)
            filename = str(postid) + os.path.splitext(secure_filename(file.filename))[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            post_helper.add_image({"postid": postid, "postimage": filename})
            return jsonify({"message": "Image uploaded successfully"}), 200
        else:
            return jsonify({"message": "Invalid file type"}), 401
    except ERROR.DB_Error as e:
        return jsonify({"message": f"Error uploading image: {e}"}), 401


@post_api_bp.route('/api/delete_post/<int:postid>', methods=['POST'])
def delete_post(postid):
    data = {"postid": postid}
    post = post_helper.get_post(data)
    userid = user_service.get_userid(session['username'])
    if int(post['userid']) == int(userid):
        try:
            post_helper.delete_post(data)
            return jsonify({"message": "Post deleted successfully"}), 200
        except ERROR.DB_Error as e:
            return jsonify({"message": f"Error deleting post: {e}"}), 401
    else:
        return jsonify({"message": f"Error deleting post: {e}"}), 401
