from nba_api.stats.endpoints import leaguedashteamstats 
from nba_api.stats.endpoints import leaguedashplayerstats 
from pathlib import Path
from requests.exceptions import ReadTimeout
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
timeout_seasons = []

failed_number1 = 0
failed_number2 = 0

try:
    for i in range(1996, 2026):
        shortyear = (i + 1) % 100
        data = seasoner.transfer_stats(f"{i}-{shortyear:02d}")
except ReadTimeout:
    for i in range(1996, 2006):
        shortyear = (i + 1) % 100
        data = seasoner.transfer_stats(f"{i}-{shortyear:02d}")
    for i in range(2006, 2016):
        shortyear = (i + 1) % 100
        data = seasoner.transfer_stats(f"{i}-{shortyear:02d}")
    for i in range(2016, 2026):
        shortyear = (i + 1) % 100
        data = seasoner.transfer_stats(f"{i}-{shortyear:02d}")
except ReadTimeout:
    i = 1996
    for k in range (1996, 2026):
        for i in range(i, k + 1):
            if i == 2026:
                i = 1996
                break
            shortyear = (i + 1) % 100
            data = seasoner.transfer_stats(f"{i}-{shortyear:02d}")
            if ReadTimeout:
                failed_number1 = i
                failed_number2 = shortyear
                timeout_seasons.append(f"{failed_number1}-{failed_number2}")
                i += 1
                continue
            i += 1