from nba_api.stats.endpoints import leaguedashteamstats 
from nba_api.stats.endpoints import leaguedashplayerstats 
from pathlib import Path
import json

with open("starters\\stats.json", "r") as f:
    traditional = json.load(f)

class TraditionalStats:
    def __init__(self):
        self.season = ""

    def get_season(self, seasons):
       self.season = seasons
       return self.season

    def get_team_stats(self, seasons):
        teams = leaguedashteamstats.LeagueDashTeamStats(
        season = self.get_season(seasons),
        season_type_all_star = traditional["traditional"]["season_type_all_star"]
        )

        team_data_frames = teams.get_data_frames()[0]

        return team_data_frames

    def get_player_stats(self, seasons):
         players = leaguedashplayerstats.LeagueDashPlayerStats(season = self.get_season(seasons), 
                season_type_all_star = traditional["traditional"]["season_type_all_star"]
            )
        
         player_data_frames = players.get_data_frames()[0]

         return player_data_frames

    def transfer_stats(self, season):
        team_data = self.get_team_stats(season)
        team_folder = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\gear3\\NBA-Prophet\\data\\unfiltered\\teams\\traditional")
        team_folder.mkdir(parents = True, exist_ok = True)
        team_file_path = team_folder / f"{season}_traditional_stats.csv"
        team_data.to_csv(team_file_path, index = False)

        player_data = self.get_player_stats(season)
        player_folder = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\gear3\\NBA-Prophet\\data\\unfiltered\\players\\traditional")
        player_folder.mkdir(parents = True, exist_ok = True)
        player_file_path = player_folder / f"{season}_traditional_stats.csv"
        player_data.to_csv(player_file_path, index = False)

        return "Done"

seasoner = TraditionalStats()
for i in range(2020, 2026):
    shortyear = (i + 1) % 100
    data = seasoner.transfer_stats(f"{i}-{shortyear:02d}")