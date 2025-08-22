from flask import Blueprint, request, jsonify
from src.services.api_football import APIFootballService
from src.services.analysis_engine import AnalysisEngine

analysis_bp = Blueprint('analysis', __name__)
api_service = APIFootballService()
analysis_engine = AnalysisEngine()

@analysis_bp.route('/search-teams', methods=['GET'])
def search_teams():
    """Rechercher des équipes par nom"""
    team_name = request.args.get('name', '')
    
    if not team_name:
        return jsonify({'error': 'Le nom de l\'équipe est requis'}), 400
    
    # Utiliser l'API réelle pour rechercher les équipes
    teams = api_service.search_teams(team_name)
    
    return jsonify({"teams": teams})

@analysis_bp.route('/analyze-match', methods=['POST'])
def analyze_match():
    """Analyser un match entre deux équipes"""
    data = request.get_json()
    
    if not data or 'team1_id' not in data or 'team2_id' not in data:
        return jsonify({'error': 'Les IDs des deux équipes sont requis'}), 400
    
    team1_id = data['team1_id']
    team2_id = data['team2_id']
    
    try:
        # Données simulées pour la démo
        # En production, ces données viendraient de l'API réelle
        
        # Forme récente simulée
        team1_form = {
            'score': 75.5,
            'wins': 7,
            'draws': 2,
            'losses': 1,
            'goals_for': 18,
            'goals_against': 8,
            'goal_difference': 10
        }
        
        team2_form = {
            'score': 60.2,
            'wins': 5,
            'draws': 3,
            'losses': 2,
            'goals_for': 14,
            'goals_against': 12,
            'goal_difference': 2
        }
        
        # Historique H2H simulé
        h2h_analysis = {
            'total_matches': 15,
            'team1_wins': 6,
            'team2_wins': 4,
            'draws': 5,
            'team1_win_percentage': 40.0,
            'team2_win_percentage': 26.67,
            'draw_percentage': 33.33,
            'avg_goals_team1': 1.8,
            'avg_goals_team2': 1.4
        }
        
        # Statistiques d'équipe simulées
        team1_stats = {
            'goals': {
                'for': {'average': {'total': 2.1}},
                'against': {'average': {'total': 0.9}}
            },
            'fixtures': {
                'wins': {'home': 8, 'away': 5}
            }
        }
        
        team2_stats = {
            'goals': {
                'for': {'average': {'total': 1.6}},
                'against': {'average': {'total': 1.3}}
            },
            'fixtures': {
                'wins': {'home': 6, 'away': 4}
            }
        }
        
        # Analyses
        prediction = analysis_engine.predict_match_outcome(team1_form, team2_form, h2h_analysis)
        team1_analysis = analysis_engine.analyze_team_strengths_weaknesses(team1_stats)
        team2_analysis = analysis_engine.analyze_team_strengths_weaknesses(team2_stats)
        
        # Récupérer les informations des équipes via l'API
        team1_data = api_service.search_teams_by_id(team1_id)
        team2_data = api_service.search_teams_by_id(team2_id)
        
        team1_name = team1_data.get('name', f'Équipe {team1_id}') if team1_data else f'Équipe {team1_id}'
        team2_name = team2_data.get('name', f'Équipe {team2_id}') if team2_data else f'Équipe {team2_id}'
        
        # Récupérer les données réelles des équipes
        team1_fixtures = api_service.get_team_fixtures(team1_id, last=10)
        team2_fixtures = api_service.get_team_fixtures(team2_id, last=10)
        
        # Récupérer l'historique H2H
        h2h_fixtures = api_service.get_head_to_head(team1_id, team2_id)
        
        # Analyser la forme récente
        team1_form = analysis_engine.analyze_recent_form(team1_fixtures, team1_id)
        team2_form = analysis_engine.analyze_recent_form(team2_fixtures, team2_id)
        
        # Analyser l'historique H2H
        h2h_analysis = analysis_engine.analyze_head_to_head(h2h_fixtures, team1_id, team2_id)
        
        # Générer la prédiction basée sur les données réelles
        prediction = analysis_engine.predict_match_outcome(team1_form, team2_form, h2h_analysis)
        
        # Générer des insights personnalisés
        key_insights = analysis_engine.generate_match_insights(
            team1_name, team2_name, team1_form, team2_form, h2h_analysis, prediction
        )

        result = {
            'team1_name': team1_name,
            'team2_name': team2_name,
            'form_analysis': {
                'team1': team1_form,
                'team2': team2_form
            },
            'head_to_head': h2h_analysis,
            'prediction': prediction,
            'team_analysis': {
                'team1': team1_analysis,
                'team2': team2_analysis
            },
            'key_insights': [
                "L'Équipe 1 montre une meilleure forme récente avec 75.5% de performance",
                "L'historique des confrontations est équilibré avec 33.33% de matchs nuls",
                "L'Équipe 1 a une attaque plus efficace (2.1 buts/match vs 1.6)",
                "L'Équipe 1 a également une défense plus solide (0.9 buts encaissés/match vs 1.3)"
            ]
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de l\'analyse: {str(e)}'}), 500

@analysis_bp.route('/matches-by-date', methods=['GET'])
def get_matches_by_date():
    """Récupérer les matchs par date et championnat"""
    date = request.args.get('date')
    league_id = request.args.get('league_id')
    
    if not date:
        return jsonify({'error': 'La date est requise'}), 400
    
    # Utiliser l'API réelle pour récupérer les matchs
    matches = api_service.get_fixtures_by_date(date, league_id)

    # Si aucun championnat n'est précisé, ne garder que les 5 grands championnats européens
    if not league_id:
        top_leagues = {39, 140, 135, 78, 61}  # Premier League, La Liga, Serie A, Bundesliga, Ligue 1
        matches = [m for m in matches if m.get('league', {}).get('id') in top_leagues]
    else:
        try:
            league_id_int = int(league_id)
            matches = [m for m in matches if m.get('league', {}).get('id') == league_id_int]
        except Exception:
            pass
    
    return jsonify({"matches": matches})

@analysis_bp.route('/leagues', methods=['GET'])
def get_leagues():
    """Récupérer la liste des championnats disponibles"""
    
    # Données simulées pour la démo
    demo_leagues = [
        {
            'league': {
                'id': 39,
                'name': 'Premier League',
                'type': 'League',
                'logo': 'https://media.api-sports.io/football/leagues/39.png'
            },
            'country': {
                'name': 'England',
                'code': 'GB',
                'flag': 'https://media.api-sports.io/flags/gb.svg'
            }
        },
        {
            'league': {
                'id': 140,
                'name': 'La Liga',
                'type': 'League',
                'logo': 'https://media.api-sports.io/football/leagues/140.png'
            },
            'country': {
                'name': 'Spain',
                'code': 'ES',
                'flag': 'https://media.api-sports.io/flags/es.svg'
            }
        },
        {
            'league': {
                'id': 135,
                'name': 'Serie A',
                'type': 'League',
                'logo': 'https://media.api-sports.io/football/leagues/135.png'
            },
            'country': {
                'name': 'Italy',
                'code': 'IT',
                'flag': 'https://media.api-sports.io/flags/it.svg'
            }
        },
        {
            'league': {
                'id': 78,
                'name': 'Bundesliga',
                'type': 'League',
                'logo': 'https://media.api-sports.io/football/leagues/78.png'
            },
            'country': {
                'name': 'Germany',
                'code': 'DE',
                'flag': 'https://media.api-sports.io/flags/de.svg'
            }
        },
        {
            'league': {
                'id': 61,
                'name': 'Ligue 1',
                'type': 'League',
                'logo': 'https://media.api-sports.io/football/leagues/61.png'
            },
            'country': {
                'name': 'France',
                'code': 'FR',
                'flag': 'https://media.api-sports.io/flags/fr.svg'
            }
        }
    ]
    
    return jsonify({'leagues': demo_leagues})

@analysis_bp.route('/team-details/<int:team_id>', methods=['GET'])
def get_team_details(team_id):
    """Obtenir les détails d'une équipe"""
    
    # Données simulées pour la démo
    team_details = {
        'id': team_id,
        'name': f'Équipe {team_id}',
        'country': 'France',
        'founded': 1900,
        'logo': 'https://via.placeholder.com/100',
        'venue': {
            'name': f'Stade de l\'Équipe {team_id}',
            'capacity': 50000
        },
        'recent_form': {
            'matches': [
                {'opponent': 'Adversaire 1', 'result': 'W', 'score': '2-1'},
                {'opponent': 'Adversaire 2', 'result': 'W', 'score': '3-0'},
                {'opponent': 'Adversaire 3', 'result': 'D', 'score': '1-1'},
                {'opponent': 'Adversaire 4', 'result': 'W', 'score': '2-0'},
                {'opponent': 'Adversaire 5', 'result': 'L', 'score': '0-2'}
            ]
        },
        'season_stats': {
            'matches_played': 25,
            'wins': 15,
            'draws': 6,
            'losses': 4,
            'goals_for': 42,
            'goals_against': 23,
            'points': 51
        }
    }
    
    return jsonify(team_details)
