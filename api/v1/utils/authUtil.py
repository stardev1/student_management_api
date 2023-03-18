from flask_jwt_extended import get_jwt_identity
from api.v1 import db
from functools import wraps
from api.v1.models import User
def teacher_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        user = db.session.query(User).get_or_404(current_user)
        if user and user.role != 'teacher':
            return {'message': 'Only teachers authorized to access this route'}, 403
        return func(*args, **kwargs)
    return wrapper