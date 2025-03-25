from flask import Blueprint, jsonify
from database.models import db

bp = Blueprint('main', __name__)

@bp.route('/health')
def health_check():
    return jsonify({"status": "healthy"})

@bp.route('/init-db')
def init_db():
    db.create_all()
    return jsonify({"message": "Database initialized"}) 