from flask import Blueprint, jsonify, request
from coursemanager.extensions import db
from coursemanager.models import Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code

@courses_bp.route('/', methods=['GET', 'POST'])
def handle_courses():
    if request.method == 'GET':
        all_courses = Course.query.all()
        return jsonify([course.to_dict() for course in all_courses]), 200

    if request.method == 'POST':
        data = request.get_json() or {}
        required_fields = ['name', 'code', 'credits', 'department_id']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'status': 'error', 'message': f'Missing fields: {", ".join(missing_fields)}'}), 400
            
        new_course = Course(
            name=data['name'], 
            code=data['code'], 
            credits=data['credits'], 
            department_id=data['department_id']
        )
        db.session.add(new_course)
        db.session.commit()
        return make_response_json(new_course.to_dict(), 201)

@courses_bp.route('/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'GET':
        return make_response_json(course.to_dict(), 200)
        
    if request.method == 'PUT':
        data = request.get_json() or {}
        course.name = data.get('name', course.name)
        course.code = data.get('code', course.code)
        course.credits = data.get('credits', course.credits)
        db.session.commit()
        return make_response_json(course.to_dict(), 200)
        
    if request.method == 'DELETE':
        db.session.delete(course)
        db.session.commit()
        return make_response_json({'message': f'Course {course_id} deleted'}, 200)

@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def get_enrolled_students(course_id):
    Course.query.get_or_404(course_id)
    enrolled_students = db.session.query(Student).join(Enrollment, Student.id == Enrollment.student_id).filter(Enrollment.course_id == course_id).all()
    return jsonify([student.to_dict() for student in enrolled_students]), 200