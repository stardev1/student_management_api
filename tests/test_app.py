import json
import pytest
from db import db
from app import create_app
from api.v1.models import User, Course, Enrollment, Student
from flask_jwt_extended import create_access_token



def test_get_all_students(client):
    """
    check if user auth and get all students
    """
    response = client.get('/api/students')
    assert response.status_code == 401  # unauthenticated request
    # create an access token for the test user
    access_token = create_access_token(identity='test_user')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/api/students', headers=headers)
    assert response.status_code == 200

def test_create_student(client):
    data = {'name': 'Test Student', 'id': 123, 'email': 'test_student@example.com'}
    response = client.post('/api/students', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401  # unauthenticated request
    # create an access token for the test user
    access_token = create_access_token(identity='test_user')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/api/students', data=json.dumps(data), headers=headers, content_type='application/json')
    assert response.status_code == 201



def test_get_all_courses(client):
    """
    check if user auth and get all students
    """
    response = client.get('/api/courses')
    assert response.status_code == 401  # unauthenticated request
    # create an access token for the test user
    access_token = create_access_token(identity='test_user')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/api/courses', headers=headers)
    assert response.status_code == 200

def test_create_course(client):
    data = {'name': 'Test course', 'teacher': 'teacher', 'credits':5}
    response = client.post('api/courses', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401  # unauthenticated request
    # create an access token for the test user
    access_token = create_access_token(identity={"username": 'test_user', "role":"teacher"})
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('api/courses', data=json.dumps(data), headers=headers, content_type='application/json')
    assert response.status_code == 201


def test_get_all_enrolled_students(client):
    """
    check if user auth and get all students
    """
    response = client.get('/api/courses')
    assert response.status_code == 401  # unauthenticated request
    # create an access token for the test user
    access_token = create_access_token(identity='test_user')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/api/courses', headers=headers)
    assert response.status_code == 200

def test_enroll_student(client):
    data = {'student_id': 1, 'course_id': 1, 'grade': 5}
    response = client.post('/api/courses', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401  # unauthenticated request
    # create an access token for the test user
    access_token = create_access_token(identity={"name": 'test_user', "role":"teacher"})
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.post('/api/enrollments', data=json.dumps(data), headers=headers, content_type='application/json')
    assert response.status_code == 201



def test_update_student(client):
    student = {'name': 'Test Student', 'id':1, 'email': 'test_student@example.com'}
   
    new_data = {'name': 'Updated Student', 'email': 'updated_student@example.com'}
    response = client.put(f'api/students/{student["id"]}', data=json.dumps(new_data), content_type='application/json')
    assert response.status_code == 401  # unauthenticated request
    # create an access token for the test user
    access_token = create_access_token(identity='test_user')
    headers = {'Authorization': f'Bearer {access_token}'}
  
    assert Student.query.first().id == 1
    response = client.get(f'/api/students/{student["id"]}', headers=headers, content_type='application/json')
    assert response.status_code == 200
    response = client.put(f'api/students/{student["id"]}', data=json.dumps(student), headers=headers, content_type='application/json')
    # print(response)
    assert response.status_code == 200



