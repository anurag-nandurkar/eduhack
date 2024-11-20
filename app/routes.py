from flask import Blueprint, request, jsonify
from . import db, bcrypt
from .models import User, Course, Collaboration

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Welcome to EduHack Backend!"})

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials!"}), 401

@main.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{"id": course.id, "title": course.title, "description": course.description} for course in courses])

@main.route('/collaborations', methods=['POST'])
def create_collaboration():
    data = request.get_json()
    if not data or not data.get('course_id') or not data.get('user_id') or not data.get('role'):
        return jsonify({"error": "Missing required fields"}), 400

    collaboration = Collaboration(course_id=data['course_id'], user_id=data['user_id'], role=data['role'])
    db.session.add(collaboration)
    db.session.commit()
    return jsonify({"message": "Collaboration created successfully!"})