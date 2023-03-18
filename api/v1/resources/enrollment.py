from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from api.v1.models import Enrollment
from api.v1 import db
from api.v1.utils.authUtil import teacher_required

enrollment_ns = Namespace('enrollments', description='Students Enrollment operations')

enrollment_serializer = enrollment_ns.model('Enrollment', {
    'id': fields.Integer(),
    'student_id': fields.Integer(required=True),
    'course_id': fields.Integer(required=True),
})

@enrollment_ns.route('')
class EnrollmentList(Resource):
    @jwt_required()
    @enrollment_ns.marshal_list_with(enrollment_serializer)
    def get(self):
        """
        Get all students enrolled in a specific course
        """
        enrollments = Enrollment.query.all()
        return enrollments
    
    @jwt_required()
    # @teacher_required
    @enrollment_ns.expect(enrollment_serializer)
    @enrollment_ns.marshal_with(enrollment_serializer, code=201)
    def post(self):
        """ 
         Enroll a student in a specific course
        """
        data = enrollment_ns.payload
        if Enrollment.query.filter_by(student_id=data['student_id'], course_id=data['course_id']).first():
       
            return {'message': 'user already enrolled'}, 400
        
        enrollment = Enrollment(student_id=data['student_id'], course_id=data['course_id'], grade=data['grade'])
        db.session.add(enrollment)
        db.session.commit()
        return enrollment, 201

@enrollment_ns.route('/<int:id>')
class EnrollmentDetail(Resource):
    @jwt_required()
    @enrollment_ns.marshal_with(enrollment_serializer)
    def get(self, id):
        """
        Get enrollment by id or return 404
        """
        enrollment = Enrollment.query.get_or_404(id)
        return enrollment
    
    @jwt_required()
    @teacher_required
    @enrollment_ns.expect(enrollment_serializer)
    @enrollment_ns.marshal_with(enrollment_serializer)
    def put(self, id):
        """
        Update enrolled user or shift to other 
        """
        print(id)
        enrollment = Enrollment.query.get_or_404(id)
        data = enrollment_ns.payload
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
    
@enrollment_ns.route('/<int:student_id>/courses/<int:course_id>')
class StudentCourseDetail(Resource):
    @jwt_required()
    @enrollment_ns.marshal_with(enrollment_serializer)
    def get(self, student_id, course_id):
        """
        Get specific student enrolled in specific course
        """
        enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
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