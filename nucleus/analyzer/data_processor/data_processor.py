import pandas
from pathlib import Path

class DataProcessor:
    def __init__(self):
        self.trad_team_unfiltered_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\traditional")
        self.trad_player_unfiltered_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\traditional")
        self.adv_team_unfiltered_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\advanced")
        self.adv_player_unfiltered_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\advanced")
        self.team_filtered_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\filtered\\teams")
        self.player_filtered_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\filtered\\players")

        self.team_identifiers = ["TEAM_ID", "TEAM_NAME"]
        self.player_identifiers = ["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"]

    def season_adder(self):
        files = {}

        for file in self.trad_team_unfiltered_path.iterdir():
            file_reader = pandas.read_csv(file)
            season = file.name.split("_")[0]
            file_reader["SEASON"] = season
            files[("team", "traditional", season)] = file_reader

        for file in self.adv_team_unfiltered_path.iterdir():
            file_reader = pandas.read_csv(file)
            season = file.name.split("_")[0]
            file_reader["SEASON"] = season
            files[("team", "advanced", season)] = file_reader

        for file in self.trad_player_unfiltered_path.iterdir():
            file_reader = pandas.read_csv(file)
            season = file.name.split("_")[0]
            file_reader["SEASON"] = season
            files[("player", "traditional", season)] = file_reader

        for file in self.adv_player_unfiltered_path.iterdir():
            file_reader = pandas.read_csv(file)
            season = file.name.split("_")[0]
            file_reader["SEASON"] = season
            files[("player", "advanced", season)] = file_reader

        return files

    def check_duplicate_rows(self):
        files = self.season_adder()

        for dataframes in files.values():
            dataframes.drop_duplicates(inplace = True)

        return files

    def check_missing_rows(self):
        files = self.check_duplicate_rows()

        for file_code, file in files.items():
            if file_code[0] == "team":
                for items in range(0, len(self.team_identifiers)):
                    if file[self.team_identifiers[items]].isna().any():
                        print(f"{self.team_identifiers[items]} is missing.")
            if file_code[0] == "player":
                for items in range(0, len(self.player_identifiers)):
                    if file[self.player_identifiers[items]].isna().any():
                        print(f"{self.player_identifiers[items]} is missing.")

        return files

    def take_out_rank(self):
        files = self.check_missing_rows()

        for file in files.values():
            file_rank = [column for column in file.columns if column.endswith("_RANK")]
            file.drop(columns = file_rank, inplace = True)

        return files

    def processor(self):
        files = self.take_out_rank()

        for key, team_file in files.items():
            category, stat_type, season = key

            if category != "team" or stat_type != "traditional":
                continue

            adv_team = files[("team", "advanced", season)]

            team_file_merger = team_file.merge(adv_team, on = "TEAM_ID", how = "inner", suffixes = ("_trad", "_adv"), validate = "one_to_one")

            same_team_columns = set(team_file.columns) & set(adv_team.columns)
            same_team_columns.discard("TEAM_ID")

            for team_column in same_team_columns:
                trad_team_column = f"{team_column}_trad"
                adv_column = f"{team_column}_adv"

                if team_file_merger[trad_team_column].equals(team_file_merger[adv_column]):
                    team_file_merger.rename(columns = {trad_team_column: team_column}, inplace = True)
                    team_file_merger.drop(columns = [adv_column], inplace = True)
                    
            self.team_filtered_path.mkdir(parents = True, exist_ok = True)
            team_file_path = self.team_filtered_path / f"{season}_filtered_team_stats.csv"
            team_file_merger.to_csv(team_file_path, index = False)

        for key, player_file in files.items():
            category, stat_type, season = key
        
            if category != "player" or stat_type != "traditional":
                continue
        
            adv_player = files[("player", "advanced", season)]
        
            player_file_merger = player_file.merge(adv_player, on = "PLAYER_ID", how = "inner", suffixes = ("_trad", "_adv"), validate = "one_to_one")
        
            same_player_columns = set(player_file.columns) & set(adv_player.columns)
            same_player_columns.discard("PLAYER_ID")
        
            for player_column in same_player_columns:
                trad_player_column = f"{player_column}_trad"
                adv_column = f"{player_column}_adv"
        
                if player_file_merger[trad_player_column].equals(player_file_merger[adv_column]):
                    player_file_merger.rename(columns = {trad_player_column: player_column}, inplace = True)
                    player_file_merger.drop(columns = [adv_column], inplace = True)

            self.player_filtered_path.mkdir(parents = True, exist_ok = True)
            player_file_path = self.player_filtered_path / f"{season}_filtered_player_stats.csv"
            player_file_merger.to_csv(player_file_path, index = False)       

processor = DataProcessor()
processor.processor()

