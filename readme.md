# Student Management API
## This is a REST API for managing students, courses, enrollments, grades, and GPAs.

## Installation
1. Clone the repository:
    `git clone https://github.com/stardev1/student-management-api.git`
2. Install the requirements:
    1. Go to project directory: 
        `cd student-management-api`
    2. Install poetry: 
        `pip install poetry`
    3. Install dependancy
        `poetry install`
3. Run the Flask-restx app:
    `poetry run python -m app`

The API will be available at `http://localhost:5000/api`

## API Endpoints

### Swagger UI
    `GET api/`: Get Swagger UI

### Students
    `GET /api/students`: Get all students
    `GET /api/students/{id}`: Get a specific student by ID
    `POST /api/students`: Create a new student
    `PUT /api/students/{id}`: Update an existing student by ID
    `DELETE /api/students/{id}`: Delete an existing student by ID

### Courses
    `GET /api/courses`: Get all courses
    `GET /api/courses/{id}`: Get a specific course by ID
    `POST /api/courses`: Create a new course
    `PUT /api/courses/{id}`: Update an existing course by ID
    `DELETE /api/courses/{id}`: Delete an existing course by ID

### Enrollments
    `GET /api/enrollments/{student_id}/courses/{course_id}`: Get all students enrolled in a specific course
    `POST /api/enrollments/{student_id}/courses/{course_id}`: Enroll a student in a specific course
    `DELETE /api/enrollments/{student_id}/courses/{course_id}`: Unenroll a student from a specific course
### Grades
    `GET /api/grade/{student_id}`: Get all grades for a specific student
    `GET /api/students/{id}/courses/{course_id}/grade`: Get the grade for a specific student in a specific course
    `POST /api/grade/{student_id}/courses/{course_id}/grade`: Add or update the grade for a specific student in a specific course
    `DELETE /api/grade/{student_id}/courses/{course_id}/grade`: Remove the grade for a specific student in a specific course
### GPAs
    `GET /api/students/{id}/gpa`: Get the GPA for a specific student
### Tests
    `run test FLASK_DEBUG=True poetry run python -m pytest tests/
    
