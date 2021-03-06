"""Author: Jarand Nikolai Jansen"""

from flask import jsonify, request
from .. import app
from ..utils.auth import generate_token, verify_token, email_is_valid
from ..utils.tools import valid_register_input
from ..utils.db_handler import get_user_with_email_and_password
from ..utils.db_handler import insert_user_to_db, user_already_in_db

@app.route("/login", methods=['POST'])
def login():
    """Fill in docstring"""
    try:
        incoming = request.get_json()
        if email_is_valid(incoming["email"]) is False:
            return jsonify(error=True), 400
        user = get_user_with_email_and_password(
            incoming["email"].lower().strip(), incoming["password"]
        )
        if user:
            return jsonify(generate_token(user))

        return jsonify(error=True,
                       errorMessage=
                       "That user do not exist. Are you certain of your existance?"), 404
    except:
        return jsonify(error=True), 500

@app.route("/is_token_valid", methods=["POST"])
def is_token_valid():
    """Fill in docstring"""
    try:
        incoming = request.get_json()
        is_valid = verify_token(incoming["token"])
        if is_valid:
            return jsonify(token_is_valid=True)
        else:
            return jsonify(token_is_valid=False), 403
    except:
        return jsonify(error=True), 404

@app.route('/register', methods=['POST'])
def create_user():
    """Fill in docstring"""
    try:
        incoming = request.get_json()
        #Sanitizes input before db-lookup - avoid db injections.
        if email_is_valid(incoming["email"]) is False:
            return jsonify(error=True), 404
        if user_already_in_db(incoming['email']):
            return jsonify(message="email already exists"), 400
        if valid_register_input(incoming) is False:
            return jsonify(message="Input not valid"), 400
        user = insert_user_to_db(incoming)
        if user:
            return jsonify(generate_token(user)), 201
        else:
            return jsonify(error=True), 404
    #If any of the actions above fail, this stops the server from crashing.
    except:
        return jsonify(error=True), 500
