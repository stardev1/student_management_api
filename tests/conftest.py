import pytest
from app import create_app
from db import db
from api.v1.models import User, Course

@pytest.fixture(scope='module')
def client():
    app = create_app(False)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # create test user
            # db = cre
            test_user = User(username='test_user', password='password', role="teacher")
            print(test_user)
            db.session.add(test_user)
            db.session.commit()
            # create test course
            # test_course = Course(name='Test Course', teacher='Test Teacher', credits= 3)
            # db.session.add(test_course)
            # db.session.commit()
        
            yield client
            db.session.remove()
            db.drop_all()



# import pytest

# from app import create_app
# from db import db

# @pytest.fixture(scope='module')
# def app():
#     app = create_app(False)

#     with app.app_context():
#         db.create_all()
#         test_user = User(username='test_user', password='password', role="teacher")
#         print(test_user)
#         db.session.add(test_user)
#         db.session.commit()

#     yield app

# @pytest.fixture()
# def client(app):
#     return app.test_client()