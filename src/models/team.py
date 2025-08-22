from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), nullable=True)
    country = db.Column(db.String(50), nullable=True)
    founded = db.Column(db.Integer, nullable=True)
    logo = db.Column(db.String(255), nullable=True)
    venue_name = db.Column(db.String(100), nullable=True)
    venue_capacity = db.Column(db.Integer, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'api_id': self.api_id,
            'name': self.name,
            'code': self.code,
            'country': self.country,
            'founded': self.founded,
            'logo': self.logo,
            'venue_name': self.venue_name,
            'venue_capacity': self.venue_capacity
        }

