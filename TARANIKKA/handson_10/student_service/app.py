from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
# Step 98: Dedicated separate database instance for Student Service
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

# Steps 100 & 101: Enrollment verification with circuit fallbacks
@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
        
    data = request.json
    course_id = data.get('course_id')
    
    # Step 100: Call Course Service to verify course existence via request library
    try:
        response = requests.get(f"http://localhost:5001/api/courses/{course_id}", timeout=3)
        if response.status_code == 404:
            return jsonify({"error": "Cannot enroll. Course does not exist."}), 400
    except requests.exceptions.ConnectionError:
        # Step 101: Handle Downstream Service Outage Gracefully
        return jsonify({"error": "Service Unavailable. Course verification system is down."}), 503

    enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({"message": "Enrollment processed successfully", "enrollment_id": enrollment.id}), 201

@app.route('/api/students/', methods=['POST'])
def create_student():
    data = request.json
    new_student = Student(name=data['name'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"id": new_student.id, "name": new_student.name}), 201

if __name__ == '__main__':
    # Step 98: Bind explicitly to port 5002
    app.run(port=5002, debug=True)