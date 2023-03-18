from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import jwt_required
from api.v1.models import Enrollment
from api.v1 import db
from api.v1.utils.authUtil import teacher_required

grade_ns = Namespace('grade', description='Students Enrollment operations')

grade_serializer = grade_ns.model('Enrollment', {
    'id': fields.Integer(),
    'student_id': fields.Integer(required=True),
    'course_id': fields.Integer(required=True),
    'grade': fields.Float()
})



@grade_ns.route('<int:student_id>')
class GradeDetail(Resource):
    @jwt_required()
    @grade_ns.marshal_with(grade_serializer)
    def get(self, student_id):
        """
        Get student grade by student id or return 404
        """
        grade = Enrollment.query.filter_by(student_id=student_id).all()
        return grade
    


    
@grade_ns.route('<int:student_id>/courses/<int:course_id>')
class StudentCourseDetail(Resource):
    @jwt_required()
    @grade_ns.marshal_with(grade_serializer)
    def get(self, student_id, course_id):
        """
        Get specific student grade in specific course
        """
        grade = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
        return grade
    
    @jwt_required()
    @teacher_required
    @grade_ns.expect(grade_serializer)
    @grade_ns.marshal_with(grade_serializer)
    def put(self, student_id, course_id):
        """
        Update  student grade
        """
        stgrade = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
        data = grade_ns.payload
        stgrade.grade = data.get('grade', stgrade.grade)
        db.session.commit()
        return stgrade

    @jwt_required()
    @teacher_required
    def delete(self, student_id, course_id):
        """
        remove specific student grade from specific course
        """
        stgrade = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first_or_404()
        stgrade.grade = 0
        db.session.commit()
        return '', 204