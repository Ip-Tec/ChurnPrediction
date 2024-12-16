from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship: A user can have many data files
    data_files = db.relationship('DataModel', backref='user', lazy=True)  

    def __init__(self, email, password):
        self.email = email
        self.password = generate_password_hash(password)

    # Save user to database
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Check password
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    # Find user by email
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    # Find user by ID
    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.get(user_id)

    # Delete user
    def delete(self):
        db.session.delete(self)
        db.session.commit()
