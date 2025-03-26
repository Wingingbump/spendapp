from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import db, User
from datetime import datetime, timedelta
import jwt
import os

router = Blueprint('auth', __name__)

SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

@router.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')

        if not email or not password:
            return jsonify({"detail": "Email and password are required"}), 400

        # Check if user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"detail": "Email already registered"}), 400

        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "email": email}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"detail": str(e)}), 500

@router.route('/token', methods=['POST'])
def login():
    try:
        data = request.form
        email = data.get('username')
        password = data.get('password')

        if not email or not password:
            return jsonify({"detail": "Email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.hashed_password, password):
            return jsonify({"detail": "Incorrect email or password"}), 401

        access_token = create_access_token(data={"sub": user.email})
        return jsonify({
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500

@router.route('/me', methods=['GET'])
def read_users_me():
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"detail": "Invalid authentication credentials"}), 401

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            email = payload.get("sub")
        except jwt.ExpiredSignatureError:
            return jsonify({"detail": "Token has expired"}), 401
        except jwt.JWTError:
            return jsonify({"detail": "Invalid token"}), 401

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"detail": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        })

    except Exception as e:
        return jsonify({"detail": str(e)}), 500 