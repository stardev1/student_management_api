from . import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    teacher = db.Column(db.String(50), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course {self.name}>'