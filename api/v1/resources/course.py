from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from api.v1.models import Course
from api.v1 import db
from api.v1.utils.authUtil import teacher_required

course_ns = Namespace('courses', description='Courses operations')

course_serializer = course_ns.model('Course', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'teacher': fields.String(required=True),
    'credits': fields.Integer(required=True)
})

student_serializer = course_ns.model('Student', {
    'id': fields.Integer(),
    'name': fields.String(required=True),
    'email': fields.String(required=True)
})

@course_ns.route('')
class CourseList(Resource):
    @jwt_required()
    @course_ns.marshal_list_with(course_serializer)
    def get(self):
        """
        Get all courses
        """
        courses = Course.query.all()
        return courses
    
    @jwt_required()
    # @teacher_required
    @course_ns.expect(course_serializer)
    @course_ns.marshal_with(course_serializer, code=201)
    def post(self):
        """
        Create a new course
        """
        data = course_ns.payload
        course = Course(name=data['name'], teacher=data['teacher'], credits=data['credits'])
        db.session.add(course)
        db.session.commit()
        return course, 201
    
@course_ns.route('/<int:id>')
class CourseDetail(Resource):
    @jwt_required()
    @course_ns.marshal_with(course_serializer)
    def get(self, id):
        """
        Get a specific course by ID
         or return 404
        """
        course = Course.query.get_or_404(id)
        return course
    
    @jwt_required()
    @teacher_required
    @course_ns.expect(course_serializer)
    @course_ns.marshal_with(course_serializer)
    def put(self, id):
        """
        Update an existing course by ID
        or return 404
        """
        course = Course.query.get_or_404(id)
        data = course_ns.payload
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
    
@course_ns.route('/<int:course_id>/students')
class CourseStudentList(Resource):
    @jwt_required()
    @course_ns.marshal_list_with(student_serializer)
    def get(self, course_id):
        """
        Get all students enrolled in a specific course
        """
        course = Course.query.get_or_404(course_id)
        students = [enrollment.student for enrollment in course.enrollments]
        return students
