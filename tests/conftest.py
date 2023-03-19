import pytest
from app import create_app
from db import db
from api.v1.models import User

@pytest.fixture(scope='module')
def client():
    app = create_app(False)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
    
            test_user = User(username='test_user', password='password', role="teacher")
            db.session.add(test_user)
            db.session.commit()
        
            yield client
