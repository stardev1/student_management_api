from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from db import db



api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, version='1.0', title='Student API',
          description='A simple API to manage students')

def create_app(prod):
    

    app = Flask(__name__)
    if prod:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
        app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    else:    
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'EI9NrvpvPLrmxVTb8nyia8ApRoGYzlf5UWXClJWpxeY='
    app.config['JWT_SECRET_KEY'] = 'EI9NrvpvPLrmxVTb8nyia8ApRoGYzlf5UWXClJWpxeY='
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

    jwt = JWTManager(app)
    # from md import db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    from api.v1.resources.student import student_ns
    from api.v1.resources.user import user_ns
    from api.v1.resources.course import course_ns
    from api.v1.resources.enrollment import enrollment_ns
    from api.v1.resources.grade import grade_ns

    api.add_namespace(student_ns)
    api.add_namespace(user_ns)
    api.add_namespace(course_ns)
    api.add_namespace(enrollment_ns)
    api.add_namespace(grade_ns)

    app.register_blueprint(api_bp)


    return app
