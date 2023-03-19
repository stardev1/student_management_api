from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from api.v1.models import User
from db import db

user_ns = Namespace('users', description='Users operations')
user_serializer = user_ns.model('User', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(enum=["student", "teacher"], required=True)
})


signup_user_serializer = user_ns.model('Signup', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'confirm_password': fields.String(required=True),
    'role': fields.String(enum=["student", "teacher"], required=True)
})

login_user_serializer = user_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})

@user_ns.route('/signup')
class Signup(Resource):
    @user_ns.expect(signup_user_serializer)
    def post(self):
        data = user_ns.payload
        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']
        role = data['role']

       
        # if db.session.query(User).filter_by(username=username).first():
        #     return {'message': 'Username already taken'}, 400

        if password != confirm_password:
            return {'message': 'Passwords do not match'}, 400

        hashed_password = generate_password_hash(password, method='sha256')
        user = User(username=username, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

@user_ns.route('/login')
class Login(Resource):
    @user_ns.expect(login_user_serializer)
    def post(self):
        data = user_ns.payload
        username = data['username']
        password = data['password']

        user = db.session.query(User).filter_by(username=username).first()
        if not user or not check_password_hash(user.password, password):
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200

@user_ns.route('/me')
class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = db.session.query(User).get_or_404(current_user)
        newDict = {**user.__dict__}
        del newDict['_sa_instance_state']
        return newDict, 200