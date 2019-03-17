"""This is the docstring"""
import datetime
from flask import jsonify, request, g
from ..utils.auth import requires_auth
from ..utils.tools import fileUpload
from ..utils.db_handler import insert_post_to_db, find_related_posts
from .. import app


@app.route('/post', methods=['GET'])
@requires_auth
def get_posts():
    """Hei"""
    email = g.current_user["email"]
    posts = find_related_posts(email)
    if posts:
        return jsonify(posts), 200
    return jsonify(error='Could not fetch any posts'), 404


@app.route('/post', methods=['POST'])
@requires_auth
def post_posts():
    """sefsef"""
    try:
        email = g.current_user["email"]
        #print("The current user is: " + email)
        #print(request.files)
        now = datetime.datetime.now()
        post = {
            'user_id' : email,
            'created' : now,
            'text' : "",
            'images' : [],
            'comments' : []
        }
        if request.form['content_text']:
            post['text'] = request.form['content_text']

        if request.files['file_0']:
            for file in request.files:
                print(request.files[file])
                filepath, filename = fileUpload(request.files[file])
                post['images'].append({
                    'filepath' : filepath,
                    'filename' : filename
                })
        post_id = insert_post_to_db(post)
        if post_id:
            #If the post is successful make sure to insert a post reference
            #into users posts
            posts = find_related_posts(email)
            print(posts)
            return jsonify(posts), 200
        return jsonify(error='Something went horribly wrong.'), 400

    except ValueError as err:
        return jsonify(error="Request did not receive the expected value: " + err), 500