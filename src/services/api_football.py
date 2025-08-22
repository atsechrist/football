import requests
import os
from typing import Dict, List, Optional

class APIFootballService:
    def __init__(self):
        # Pour la démo, nous utiliserons une clé API fictive
        # En production, cette clé devrait être stockée dans les variables d'environnement
        self.api_key = "83556e6bab04253125b71e52762141ff"
        self.base_url = 'https://v3.football.api-sports.io'
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': 'v3.football.api-sports.io'
        }
    
    def search_teams(self, team_name: str) -> List[Dict]:
        """Rechercher des équipes par nom"""
        try:
            url = f"{self.base_url}/teams"
            params = {'search': team_name}
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', [])
            else:
                print(f"Erreur API: {response.status_code}")
                return []
        except Exception as e:
            print(f"Erreur lors de la recherche d'équipes: {e}")
            return []
    
    def get_team_fixtures(self, team_id: int, season: int = 2024, last: int = 10) -> List[Dict]:
        """Récupérer les derniers matchs d'une équipe"""
        try:
            url = f"{self.base_url}/fixtures"
            params = {
                'team': team_id,
                'season': season,
                'last': last
            }
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', [])
            else:
                print(f"Erreur API: {response.status_code}")
                return []
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs: {e}")
            return []
    
    def get_head_to_head(self, team1_id: int, team2_id: int) -> List[Dict]:
        """Récupérer l'historique des confrontations entre deux équipes"""
        try:
            url = f"{self.base_url}/fixtures/headtohead"
            params = {
                'h2h': f"{team1_id}-{team2_id}"
            }
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', [])
            else:
                print(f"Erreur API: {response.status_code}")
                return []
        except Exception as e:
            print(f"Erreur lors de la récupération du H2H: {e}")
            return []
    
    def get_match_statistics(self, fixture_id: int) -> List[Dict]:
        """Récupérer les statistiques d'un match"""
        try:
            url = f"{self.base_url}/fixtures/statistics"
            params = {'fixture': fixture_id}
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', [])
            else:
                print(f"Erreur API: {response.status_code}")
                return []
        except Exception as e:
            print(f"Erreur lors de la récupération des statistiques: {e}")
            return []
    
    def get_team_statistics(self, team_id: int, league_id: int, season: int = 2024) -> Dict:
        """Récupérer les statistiques d'une équipe pour une saison"""
        try:
            url = f"{self.base_url}/teams/statistics"
            params = {
                'team': team_id,
                'league': league_id,
                'season': season
            }
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', {})
            else:
                print(f"Erreur API: {response.status_code}")
                return {}
        except Exception as e:
            print(f"Erreur lors de la récupération des statistiques d'équipe: {e}")
            return {}



    def get_fixtures_by_date(self, date: str, league_id: Optional[int] = None) -> List[Dict]:
        """Récupérer les matchs par date et optionnellement par championnat"""
        try:
            url = f"{self.base_url}/fixtures"
            params = {
                'date': date,
                'timezone': 'Europe/Paris' # Assurez-vous que le fuseau horaire est correct
            }
            if league_id:
                params['league'] = league_id
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', [])
            else:
                print(f"Erreur API: {response.status_code}")
                return []
        except Exception as e:
            print(f"Erreur lors de la récupération des matchs par date: {e}")
            return []




    def get_leagues(self) -> List[Dict]:
        """Récupérer la liste des championnats disponibles"""
        try:
            url = f"{self.base_url}/leagues"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code == 200:
                data = response.json()
                # Filtrer pour inclure seulement les 5 grands championnats européens
                # IDs: Premier League (39), La Liga (140), Serie A (135), Bundesliga (78), Ligue 1 (61)
                european_leagues_ids = [39, 140, 135, 78, 61]
                filtered_leagues = [league for league in data.get("response", []) 
                                    if league["league"]["id"] in european_leagues_ids]
                return filtered_leagues
            else:
                print(f"Erreur API: {response.status_code}")
                return []
        except Exception as e:
            print(f"Erreur lors de la récupération des championnats: {e}")
            return []



    def search_teams_by_id(self, team_id: int) -> Dict:
        """Rechercher une équipe par son ID"""
        try:
            url = f"{self.base_url}/teams"
            params = {'id': team_id}
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                teams = data.get('response', [])
                if teams:
                    return teams[0].get('team', {})
                return {}
            else:
                print(f"Erreur API: {response.status_code}")
                return {}
        except Exception as e:
            print(f"Erreur lors de la recherche d'équipe par ID: {e}")
            return {}

