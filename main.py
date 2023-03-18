from flask import Flask, request
from flask_restx import Api, Resource, fields
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from flask_migrate import Migrate
# from md import db, Student, Course, Enrollment
from models import db
from models.user import User
from models.student import Student
from models.course import Course
from models.enrollment import Enrollment
from datetime import timedelta



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students6.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'EI9NrvpvPLrmxVTb8nyia8ApRoGYzlf5UWXClJWpxeY='
app.config['JWT_SECRET_KEY'] = 'EI9NrvpvPLrmxVTb8nyia8ApRoGYzlf5UWXClJWpxeY='
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)
# from md import db
db.init_app(app)
with app.app_context():
    db.create_all()

# migrate = Migrate(app, db)
jwt = JWTManager(app)

api = Api(app, version='1.0', title='Student Management API', description='Project based on student management system API')

student_serializer = api.model('Student', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'email': fields.String(required=True)
})

course_serializer = api.model('Course', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'teacher': fields.String(required=True),
    'credits': fields.Integer(required=True)
})

enrollment_serializer = api.model('Enrollment', {
    'id': fields.Integer(),
    'student_id': fields.Integer(required=True),
    'course_id': fields.Integer(required=True),
    'grade': fields.Float()
})

user_serializer = api.model('User', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(enum=["student", "teacher"], required=True)
})


signup_user_serializer = api.model('Signup', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'confirm_password': fields.String(required=True),
    'role': fields.String(enum=["student", "teacher"], required=True)
})

login_user_serializer = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})

def teacher_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = db.session.query(User).get_or_404(current_user)
        if user and user.role != 'teacher':
            return {'message': 'Only teachers authorized to access this route'}, 403
        return func(*args, **kwargs)
    return wrapper


@api.route('/students')
class StudentList(Resource):
    @jwt_required()
    @api.marshal_list_with(student_serializer)
    def get(self):
        """
         Get all students from database
        """
        students = Student.query.all()
        return students

    @jwt_required()
    @api.expect(student_serializer)
    @api.marshal_with(student_serializer, code=201)
    def post(self):
        """  Create a new student """
        data = api.payload
        student = Student(name=data['name'], email=data['email'])
        db.session.add(student)
        db.session.commit()
        return student, 201

@api.route('/students/<int:id>')
class StudentDetail(Resource):
    @jwt_required()
    @api.marshal_with(student_serializer)
    def get(self, id):
        "Get a specific student by ID else return 404"
        student = Student.query.get_or_404(id)
        return student
    
    @jwt_required()
    @teacher_required
    @api.expect(student_serializer)
    @api.marshal_with(student_serializer)
    def put(self, id):
        """
        Update an existing student by ID
        or return 404
        """
        student = Student.query.get_or_404(id)
        data = api.payload
        student.name = data.get('name', student.name)
        student.email = data.get('email', student.email)
        db.session.commit()
        return student

    @jwt_required()
    @teacher_required
    def delete(self, id):
        """ Delete an existing student by ID 
            or return 404
        """
        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()
        return '', 204

@api.route('/courses')
class CourseList(Resource):
    @jwt_required()
    @api.marshal_list_with(course_serializer)
    def get(self):
        """
        Get all courses
        """
        courses = Course.query.all()
        return courses
    
    @jwt_required()
    @teacher_required
    @api.expect(course_serializer)
    @api.marshal_with(course_serializer, code=201)
    def post(self):
        """
        Create a new course
        """
        data = api.payload
        course = Course(name=data['name'], teacher=data['teacher'], credits=data['credits'])
        db.session.add(course)
        db.session.commit()
        return course, 201
    
@api.route('/courses/<int:id>')
class CourseDetail(Resource):
    @jwt_required()
    @api.marshal_with(course_serializer)
    def get(self, id):
        """
        Get a specific course by ID
         or return 404
        """
        course = Course.query.get_or_404(id)
        return course
    
    @jwt_required()
    @teacher_required
    @api.expect(course_serializer)
    @api.marshal_with(course_serializer)
    def put(self, id):
        """
        Update an existing course by ID
        or return 404
        """
        course = Course.query.get_or_404(id)
        data = api.payload
        course.name = data.get('name', course.name)
        course.teacher = data.get('teacher', course.teacher)
        course.credits = data.get('credits', course.credits)
        db.session.commit()
        return course

    @jwt_required()
    @teacher_required
    def delete(self, id):
        """ Delete an existing course by ID 
            or return 404
        """
        course = Course.query.get_or_404(id)
        db.session.delete(course)
        db.session.commit()
        return '', 204
    
@api.route('/enrollments')
class EnrollmentList(Resource):
    @jwt_required()
    @api.marshal_list_with(enrollment_serializer)
    def get(self):
        """
        Get all students enrolled in a specific course
        """
        enrollments = Enrollment.query.all()
        return enrollments
    
    @jwt_required()
    @teacher_required
    @api.expect(enrollment_serializer)
    @api.marshal_with(enrollment_serializer, code=201)
    def post(self):
        """ 
         Enroll a student in a specific course
        """
        data = api.payload
        enrollment = Enrollment(student_id=data['student_id'], course_id=data['course_id'], grade=data['grade'])
        db.session.add(enrollment)
        db.session.commit()
        return enrollment, 201

@api.route('/enrollments/<int:id>')
class EnrollmentDetail(Resource):
    @jwt_required()
    @api.marshal_with(enrollment_serializer)
    def get(self, id):
        """
        Get enrollment by id or return 404
        """
        enrollment = Enrollment.query.get_or_404(id)
        return enrollment
    
    @jwt_required()
    @teacher_required
    @api.expect(enrollment_serializer)
    @api.marshal_with(enrollment_serializer)
    def put(self, id):
        """
        Update enrolled user or shift to other 
        """
        enrollment = Enrollment.query.get_or_404(id)
        data = api.payload
        enrollment.student_id = data.get('student_id', enrollment.student_id)
        enrollment.course_id = data.get('course_id', enrollment.course_id)
        enrollment.grade = data.get('grade', enrollment.grade)
        db.session.commit()
        return enrollment

    @jwt_required()
    @teacher_required
    def delete(self, id):
        """
        Unenroll a student from a specific course
        """
        enrollment = Enrollment.query.get_or_404(id)
        db.session.delete(enrollment)
        db.session.commit()
        return '', 204 ## check again here


@api.route('/courses/<int:course_id>/students')
class CourseStudentList(Resource):
    @jwt_required()
    @api.marshal_list_with(student_serializer)
    def get(self, course_id):
        """
        Get all students enrolled in a specific course
        """
        course = Course.query.get_or_404(course_id)
        students = [enrollment.student for enrollment in course.enrollments]
        return students

@api.route('/students/<int:student_id>/courses')
class StudentCourseList(Resource):
    @jwt_required()
    @api.marshal_list_with(course_serializer)
    def get(self, student_id):
        """
        Get all courses for a specific student
        """
        student = Student.query.get_or_404(student_id)
        courses = [enrollment.course for enrollment in student.enrollments]
        return courses
    
@api.route('/students/<int:student_id>/grades')
class StudentCourseList(Resource):
    @jwt_required()
    @api.marshal_list_with(enrollment_serializer)
    def get(self, student_id):
        """
        Get all  courses grade for a specific student
        """
        student = Student.query.get_or_404(student_id)
        getenrollmentGrade = [enrollment for enrollment in student.enrollments]
        return getenrollmentGrade

@api.route('/students/<int:student_id>/courses/<int:course_id>')
class StudentCourseDetail(Resource):
    @jwt_required()
    @api.marshal_with(enrollment_serializer)
    def get(self, student_id, course_id):
        """
        Get specific student enrolled in specific course
        """
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
        return enrollment

@api.route('/students/<int:student_id>/courses/<int:course_id>/grade')
class StudentCourseDetail(Resource):
    @jwt_required()
    def get(self, student_id, course_id):
        """
        Get specific student grade in specific course
        """
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
        return {"grade": enrollment.grade}
    
    @jwt_required()
    @teacher_required
    @api.expect(enrollment_serializer)
    @api.marshal_with(enrollment_serializer)
    def put(self, student_id, course_id):
        """
        Update enrolled student and course
        """
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
        data = api.payload
        enrollment.grade = data.get('grade', enrollment.grade)
        db.session.commit()
        return enrollment

    @jwt_required()
    @teacher_required
    def delete(self, student_id, course_id):
        """
        Unenroll a student from a specific course
        """
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
        db.session.delete(enrollment)
        db.session.commit()
        return '', 204
    
@api.route('/students/<int:student_id>/gpa')
class StudentGpa(Resource):
    @jwt_required()
    def get(self, student_id):
        student = Student.query.get_or_404(student_id)
        enrollments = student.enrollments
        total_credits = 0
        total_grade_points = 0
        for enrollment in enrollments:
            course_credits = enrollment.course.credits
            grade_points = enrollment.grade * course_credits
            total_credits += course_credits
            total_grade_points += grade_points
            if total_credits == 0:
                gpa = 0.0
            else:
                gpa = total_grade_points / total_credits
        return {'gpa': gpa}


@api.route('/signup')
class Signup(Resource):
    @api.expect(signup_user_serializer)
    def post(self):
        data = api.payload
        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']
        role = data['role']

       
        if db.session.query(User).filter_by(username=username).first():
            return {'message': 'Username already taken'}, 400

        if password != confirm_password:
            return {'message': 'Passwords do not match'}, 400

        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

@api.route('/login')
class Login(Resource):
    @api.expect(login_user_serializer)
    def post(self):
        data = api.payload
        username = data['username']
        password = data['password']

        user = db.session.query(User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200

@api.route('/me')
class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = db.session.query(User).get_or_404(current_user)
        newDict = {**user.__dict__}
        del newDict['_sa_instance_state']
        return newDict, 200
    



if __name__ == '__main__':
    app.run(debug=True)
