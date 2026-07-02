# coursemanager/routes.py
from flask import Blueprint, jsonify, request

# Step 39: Define the Blueprint
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# Temporary in-memory database to hold course data for testing
courses_db = []
current_id = 1

# Step 44: Helper function for consistent JSON envelope
def make_response_json(data, status_code=200):
    return jsonify({
        'status': 'success',
        'data': data
    }), status_code

# Step 39 & 42: GET all courses and POST a new course
@courses_bp.route('/', methods=['GET', 'POST'])
def handle_courses():
    global current_id
    
    if request.method == 'GET':
        # Step 41: Returns an array of courses
        return jsonify(courses_db), 200

    if request.method == 'POST':
        data = request.get_json()
        
        # Step 42: Content-Type and Field Validation
        if not data:
            return jsonify({'status': 'error', 'message': 'Invalid or missing JSON payload'}), 400
            
        required_fields = ['name', 'code', 'credits']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({
                'status': 'error', 
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Create new course object
        new_course = {
            'id': current_id,
            'name': data['name'],
            'code': data['code'],
            'credits': data['credits']
        }
        courses_db.append(new_course)
        current_id += 1
        
        return make_response_json(new_course, 201)

# Step 43: GET, PUT, and DELETE specific course by ID
@courses_bp.route('/<int:course_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_single_course(course_id):
    # Find the course
    course = next((c for c in courses_db if c['id'] == course_id), None)
    
    if not course:
        # Step 46 requirement: Unknown IDs return 404
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404

    if request.method == 'GET':
        return make_response_json(course, 200)

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'Invalid JSON payload'}), 400
            
        # Update fields if provided
        course['name'] = data.get('name', course['name'])
        course['code'] = data.get('code', course['code'])
        course['credits'] = data.get('credits', course['credits'])
        
        return make_response_json(course, 200)

    if request.method == 'DELETE':
        courses_db.remove(course)
        return make_response_json({'message': f'Course {course_id} deleted successfully'}, 200)