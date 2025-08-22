from flask_sqlalchemy import SQLAlchemy
from src.models.user import db
from datetime import datetime

class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    api_id = db.Column(db.Integer, unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    home_score = db.Column(db.Integer, nullable=True)
    away_score = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='scheduled')
    league_id = db.Column(db.Integer, nullable=False)
    season = db.Column(db.Integer, nullable=False)
    
    # Relations
    home_team = db.relationship('Team', foreign_keys=[home_team_id], backref='home_matches')
    away_team = db.relationship('Team', foreign_keys=[away_team_id], backref='away_matches')
    
    def to_dict(self):
        return {
            'id': self.id,
            'api_id': self.api_id,
            'date': self.date.isoformat() if self.date else None,
            'home_team_id': self.home_team_id,
            'away_team_id': self.away_team_id,
            'home_score': self.home_score,
            'away_score': self.away_score,
            'status': self.status,
            'league_id': self.league_id,
            'season': self.season
        }

