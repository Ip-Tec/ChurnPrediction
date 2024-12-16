from app import db
from datetime import datetime

class DataModel(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, user_id, file_name, file_path):
        self.user_id = user_id
        self.file_name = file_name
        self.file_path = file_path

    # Save data to the database
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Find all data for a user by user_id
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    # find data by name
    @classmethod
    def find_by_name(cls, file_name):
        return cls.query.filter_by(file_name=file_name).all()
    
    # Find data by ID
    @classmethod
    def find_by_id(cls, data_id):
        return cls.query.get(data_id)

    # Delete specific data
    def delete(self):
        db.session.delete(self)
        db.session.commit()
