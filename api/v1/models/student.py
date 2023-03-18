from . import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    enrollments = db.relationship('Enrollment', backref='student', lazy=True)

    def __repr__(self):
        return f'<Student {self.name}>'
