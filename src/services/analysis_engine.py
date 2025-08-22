import statistics
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class AnalysisEngine:
    """Moteur d'analyse pour les matchs de football"""
    
    def __init__(self):
        pass
    
    def calculate_form_score(self, recent_matches: List[Dict]) -> Dict:
        """Calculer le score de forme basé sur les derniers matchs"""
        if not recent_matches:
            return {'score': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'goals_for': 0, 'goals_against': 0}
        
        wins = draws = losses = 0
        goals_for = goals_against = 0
        
        for match in recent_matches:
            fixture = match.get('fixture', {})
            teams = match.get('teams', {})
            goals = match.get('goals', {})
            
            home_goals = goals.get('home', 0) or 0
            away_goals = goals.get('away', 0) or 0
            
            # Déterminer si l'équipe jouait à domicile ou à l'extérieur
            # Cette logique devra être adaptée selon la structure des données
            if home_goals > away_goals:
                wins += 1
            elif home_goals == away_goals:
                draws += 1
            else:
                losses += 1
            
            goals_for += home_goals
            goals_against += away_goals
        
        # Calcul du score de forme (3 points pour une victoire, 1 pour un nul)
        form_score = (wins * 3 + draws * 1) / (len(recent_matches) * 3) * 100
        
        return {
            'score': round(form_score, 2),
            'wins': wins,
            'draws': draws,
            'losses': losses,
            'goals_for': goals_for,
            'goals_against': goals_against,
            'goal_difference': goals_for - goals_against
        }
    
    def analyze_head_to_head(self, h2h_matches: List[Dict], team1_id: int, team2_id: int) -> Dict:
        """Analyser l'historique des confrontations directes"""
        if not h2h_matches:
            return {'total_matches': 0, 'team1_wins': 0, 'team2_wins': 0, 'draws': 0}
        
        team1_wins = team2_wins = draws = 0
        total_goals_team1 = total_goals_team2 = 0
        
        for match in h2h_matches:
            teams = match.get('teams', {})
            goals = match.get('goals', {})
            
            home_id = teams.get('home', {}).get('id')
            away_id = teams.get('away', {}).get('id')
            home_goals = goals.get('home', 0) or 0
            away_goals = goals.get('away', 0) or 0
            
            # Déterminer les buts pour chaque équipe
            if home_id == team1_id:
                team1_goals, team2_goals = home_goals, away_goals
            else:
                team1_goals, team2_goals = away_goals, home_goals
            
            total_goals_team1 += team1_goals
            total_goals_team2 += team2_goals
            
            # Déterminer le résultat
            if team1_goals > team2_goals:
                team1_wins += 1
            elif team2_goals > team1_goals:
                team2_wins += 1
            else:
                draws += 1
        
        total_matches = len(h2h_matches)
        
        return {
            'total_matches': total_matches,
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'draws': draws,
            'team1_win_percentage': round((team1_wins / total_matches) * 100, 2) if total_matches > 0 else 0,
            'team2_win_percentage': round((team2_wins / total_matches) * 100, 2) if total_matches > 0 else 0,
            'draw_percentage': round((draws / total_matches) * 100, 2) if total_matches > 0 else 0,
            'avg_goals_team1': round(total_goals_team1 / total_matches, 2) if total_matches > 0 else 0,
            'avg_goals_team2': round(total_goals_team2 / total_matches, 2) if total_matches > 0 else 0
        }
    
    def predict_match_outcome(self, team1_form: Dict, team2_form: Dict, h2h_analysis: Dict) -> Dict:
        """Prédire le résultat d'un match basé sur la forme et l'historique"""
        
        # Poids pour les différents facteurs
        form_weight = 0.6
        h2h_weight = 0.4
        
        # Score basé sur la forme récente
        form_score_team1 = team1_form.get('score', 50)
        form_score_team2 = team2_form.get('score', 50)
        
        # Score basé sur l'historique H2H
        h2h_score_team1 = h2h_analysis.get('team1_win_percentage', 33.33)
        h2h_score_team2 = h2h_analysis.get('team2_win_percentage', 33.33)
        h2h_draw_score = h2h_analysis.get('draw_percentage', 33.33)
        
        # Calcul des probabilités pondérées
        team1_probability = (form_score_team1 * form_weight + h2h_score_team1 * h2h_weight)
        team2_probability = (form_score_team2 * form_weight + h2h_score_team2 * h2h_weight)
        draw_probability = h2h_draw_score * h2h_weight + 25 * form_weight  # Base de 25% pour les nuls
        
        # Normalisation pour que la somme soit 100%
        total = team1_probability + team2_probability + draw_probability
        if total > 0:
            team1_probability = (team1_probability / total) * 100
            team2_probability = (team2_probability / total) * 100
            draw_probability = (draw_probability / total) * 100
        else:
            team1_probability = team2_probability = draw_probability = 33.33
        
        return {
            'team1_win_probability': round(team1_probability, 2),
            'team2_win_probability': round(team2_probability, 2),
            'draw_probability': round(draw_probability, 2),
            'confidence_level': self._calculate_confidence(team1_form, team2_form, h2h_analysis)
        }
    
    def _calculate_confidence(self, team1_form: Dict, team2_form: Dict, h2h_analysis: Dict) -> str:
        """Calculer le niveau de confiance de la prédiction"""
        
        # Facteurs influençant la confiance
        form_difference = abs(team1_form.get('score', 50) - team2_form.get('score', 50))
        h2h_matches = h2h_analysis.get('total_matches', 0)
        
        confidence_score = 0
        
        # Plus la différence de forme est grande, plus la confiance est élevée
        if form_difference > 30:
            confidence_score += 3
        elif form_difference > 15:
            confidence_score += 2
        else:
            confidence_score += 1
        
        # Plus il y a de matchs H2H, plus la confiance est élevée
        if h2h_matches >= 10:
            confidence_score += 3
        elif h2h_matches >= 5:
            confidence_score += 2
        else:
            confidence_score += 1
        
        # Déterminer le niveau de confiance
        if confidence_score >= 5:
            return "Élevée"
        elif confidence_score >= 3:
            return "Moyenne"
        else:
            return "Faible"
    
    def analyze_team_strengths_weaknesses(self, team_stats: Dict) -> Dict:
        """Analyser les forces et faiblesses d'une équipe"""
        
        if not team_stats:
            return {'strengths': [], 'weaknesses': [], 'overall_rating': 50}
        
        strengths = []
        weaknesses = []
        
        # Analyse des statistiques offensives
        goals_per_match = team_stats.get('goals', {}).get('for', {}).get('average', {}).get('total', 0)
        if goals_per_match > 2.0:
            strengths.append("Attaque efficace")
        elif goals_per_match < 1.0:
            weaknesses.append("Manque d'efficacité offensive")
        
        # Analyse des statistiques défensives
        goals_conceded_per_match = team_stats.get('goals', {}).get('against', {}).get('average', {}).get('total', 0)
        if goals_conceded_per_match < 1.0:
            strengths.append("Défense solide")
        elif goals_conceded_per_match > 2.0:
            weaknesses.append("Défense fragile")
        
        # Analyse de la forme à domicile/extérieur
        home_wins = team_stats.get('fixtures', {}).get('wins', {}).get('home', 0)
        away_wins = team_stats.get('fixtures', {}).get('wins', {}).get('away', 0)
        
        if home_wins > away_wins * 1.5:
            strengths.append("Forte à domicile")
        elif away_wins > home_wins * 1.5:
            strengths.append("Performante à l'extérieur")
        
        # Calcul d'une note globale (simplifiée)
        overall_rating = min(100, max(0, (goals_per_match * 20) + ((3 - goals_conceded_per_match) * 15) + 30))
        
        return {
            'strengths': strengths,
            'weaknesses': weaknesses,
            'overall_rating': round(overall_rating, 1)
        }
