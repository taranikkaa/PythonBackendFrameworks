from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Step 98: Dedicated separate database instance for Course Service
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/courses/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{"id": c.id, "name": c.name, "code": c.code} for c in courses])

@app.route('/api/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({"id": course.id, "name": course.name, "code": course.code})

@app.route('/api/courses/', methods=['POST'])
def create_course():
    data = request.json
    new_course = Course(name=data['name'], code=data['code'])
    db.session.add(new_course)
    db.session.commit()
    return jsonify({"id": new_course.id, "name": new_course.name, "code": new_course.code}), 201

if __name__ == '__main__':
    # Step 98: Bind explicitly to port 5001
    app.run(port=5001, debug=True)