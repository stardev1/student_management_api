from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from api.v1.models import Student
from api.v1 import db
from api.v1.utils.authUtil import teacher_required

student_ns = Namespace('students', description='Students operations')

student_serializer = student_ns.model('Student', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'email': fields.String(required=True)
})

enrollment_serializer = student_ns.model('Enrollment', {
    'id': fields.Integer(),
    'student_id': fields.Integer(required=True),
    'course_id': fields.Integer(required=True),
    'grade': fields.Float()
})

course_serializer = student_ns.model('Course', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'teacher': fields.String(required=True),
    'credits': fields.Integer(required=True)
})


@student_ns.route('/')
class StudentList(Resource):
    @student_ns.doc('students')
    @student_ns.marshal_list_with(student_serializer)
    @jwt_required()
    def get(self):
        """
         Get all students from database
        """
        students = Student.query.all()
        return students

    @student_ns.expect(student_serializer)
    @student_ns.marshal_with(student_serializer, code=201)
    @jwt_required()
    def post(self):
        """  Create a new student """
        data = student_ns.payload
        student = Student(name=data['name'], email=data['email'])
        db.session.add(student)
        db.session.commit()
        return student, 201

@student_ns.route('/<int:id>/')
class StudentDetail(Resource):
    @student_ns.marshal_with(student_serializer)
    @jwt_required()
    def get(self, id):
        "Get a specific student by ID else return 404"
        student = Student.query.get_or_404(id)
        return student
    
    @jwt_required()
    @student_ns.expect(student_serializer)
    @student_ns.marshal_with(student_serializer)
    def put(self, id):
        """
        Update an existing student by ID
        or return 404
        """
        print(f'Updating student with ID {id}')
        student = Student.query.get_or_404(id)
        data = student_ns.payload
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
    
@student_ns.route('/<int:student_id>/courses')
class StudentCourseList(Resource):
    @student_ns.marshal_list_with(course_serializer)
    @jwt_required()
    def get(self, student_id):
        """
        Get all courses for a specific student
        """
        student = Student.query.get_or_404(student_id)
        courses = [enrollment.course for enrollment in student.enrollments]
        return courses
    
@student_ns.route('/<int:student_id>/grades')
class StudentCourseList(Resource):
    @student_ns.marshal_list_with(enrollment_serializer)
    @jwt_required()
    def get(self, student_id):
        """
        Get all  courses grade for a specific student
        """
        student = Student.query.get_or_404(student_id)
        getenrollmentGrade = [enrollment for enrollment in student.enrollments]
        return getenrollmentGrade
    
@student_ns.route('/<int:student_id>/gpa')
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