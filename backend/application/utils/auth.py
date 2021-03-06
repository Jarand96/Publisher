from functools import wraps
import re
from flask import request, g, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from .db_handler import get_user_with_email
from .. import app

FOURTY_EIGHT_H = 172800

def generate_token(user, expiration=FOURTY_EIGHT_H):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'id': str(user["_id"]),
        'email': user["email"],
    }).decode('utf-8')
    return token

def verify_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
        #Avoid db injections by removing special characters from email.
        if email_is_valid(data["email"]) is False:
            return None
        user = get_user_with_email(data["email"])
        if user:
            return user
    except (BadSignature, SignatureExpired):
        return None

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if token:
            string_token = token.encode('ascii', 'ignore')
            user = verify_token(string_token)
            if user:
                g.current_user = user
                return f(*args, **kwargs)
        return jsonify(message="Authentication is required to access this resource"), 401
    return decorated

def email_is_valid(email):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not EMAIL_REGEX.match(email):
        return False
    return True
