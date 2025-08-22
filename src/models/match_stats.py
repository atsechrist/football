from flask_sqlalchemy import SQLAlchemy
from src.models.user import db

class MatchStats(db.Model):
    __tablename__ = 'match_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    
    # Statistiques offensives
    shots_on_goal = db.Column(db.Integer, default=0)
    shots_off_goal = db.Column(db.Integer, default=0)
    total_shots = db.Column(db.Integer, default=0)
    blocked_shots = db.Column(db.Integer, default=0)
    shots_inside_box = db.Column(db.Integer, default=0)
    shots_outside_box = db.Column(db.Integer, default=0)
    
    # Statistiques de possession
    ball_possession = db.Column(db.Float, default=0.0)
    total_passes = db.Column(db.Integer, default=0)
    passes_accurate = db.Column(db.Integer, default=0)
    passes_percentage = db.Column(db.Float, default=0.0)
    
    # Statistiques défensives
    tackles = db.Column(db.Integer, default=0)
    blocks = db.Column(db.Integer, default=0)
    interceptions = db.Column(db.Integer, default=0)
    duels_total = db.Column(db.Integer, default=0)
    duels_won = db.Column(db.Integer, default=0)
    
    # Statistiques de discipline
    fouls = db.Column(db.Integer, default=0)
    yellow_cards = db.Column(db.Integer, default=0)
    red_cards = db.Column(db.Integer, default=0)
    
    # Autres statistiques
    corner_kicks = db.Column(db.Integer, default=0)
    offsides = db.Column(db.Integer, default=0)
    
    # Relations
    match = db.relationship('Match', backref='stats')
    team = db.relationship('Team', backref='match_stats')
    
    def to_dict(self):
        return {
            'id': self.id,
            'match_id': self.match_id,
            'team_id': self.team_id,
            'shots_on_goal': self.shots_on_goal,
            'shots_off_goal': self.shots_off_goal,
            'total_shots': self.total_shots,
            'blocked_shots': self.blocked_shots,
            'shots_inside_box': self.shots_inside_box,
            'shots_outside_box': self.shots_outside_box,
            'ball_possession': self.ball_possession,
            'total_passes': self.total_passes,
            'passes_accurate': self.passes_accurate,
            'passes_percentage': self.passes_percentage,
            'tackles': self.tackles,
            'blocks': self.blocks,
            'interceptions': self.interceptions,
            'duels_total': self.duels_total,
            'duels_won': self.duels_won,
            'fouls': self.fouls,
            'yellow_cards': self.yellow_cards,
            'red_cards': self.red_cards,
            'corner_kicks': self.corner_kicks,
            'offsides': self.offsides
        }

