import pandas
from pathlib import Path
from datetime import date

class DataFilter:
    def __init__(self):
        self.trad_team_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\traditional")
        self.trad_player_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\traditional")
        self.adv_team_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\advanced")
        self.adv_player_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\advanced")
        
        self.team_identifiers = ["TEAM_ID", "TEAM_NAME"]
        self.player_identifiers = ["PLAYER_ID", "PLAYER_NAME", "TEAM_ID"]

    def season_adder(self):
        frontyear = 1996
        backyear = (frontyear + 1) % 100
        for file in self.trad_player_path.iterdir():
            if frontyear == 2026:
                frontyear = 1996
                backyear = (frontyear + 1) % 100

            file_reader = pandas.read_csv(file)
            file_reader["SEASON"] = f"{frontyear}-{backyear}"
            frontyear += 1
            backyear = (frontyear + 1) % 100

        for file in self.adv_player_path.iterdir():
            if frontyear == 2026:
                frontyear = 1996
                backyear = (frontyear + 1) % 100
        
            file_reader = pandas.read_csv(file)
            file_reader["SEASON"] = f"{frontyear}-{backyear}"
            frontyear += 1
            backyear = (frontyear + 1) % 100

        for file in self.trad_team_path.iterdir():
            if frontyear == 2026:
                frontyear = 1996
                backyear = (frontyear + 1) % 100
        
            file_reader = pandas.read_csv(file)
            file_reader["SEASON"] = f"{frontyear}-{backyear}"
            frontyear += 1
            backyear = (frontyear + 1) % 100

        for file in self.adv_team_path.iterdir():
            if frontyear == 2026:
                frontyear = 1996
                backyear = (frontyear + 1) % 100
        
            file_reader = pandas.read_csv(file)
            file_reader["SEASON"] = f"{frontyear}-{backyear}"
            frontyear += 1
            backyear = (frontyear + 1) % 100

    def check_duplicate_rows(self):
        for file in self.trad_player_path.iterdir():
            file_reader = pandas.read_csv(file)
            file_duplicate = file_reader.drop_duplicates() if file_reader.duplicated().sum() != 0 else file_reader
            file_reader = file_duplicate

        for file in self.adv_player_path.iterdir():
            file_reader = pandas.read_csv(file)
            file_duplicate = file_reader.drop_duplicates() if file_reader.duplicated().sum() != 0 else file_reader
            file_reader = file_duplicate

        for file in self.trad_team_path.iterdir():
            file_reader = pandas.read_csv(file)
            file_duplicate = file_reader.drop_duplicates() if file_reader.duplicated().sum() != 0 else file_reader
            file_reader = file_duplicate

        for file in self.adv_team_path.iterdir():
            file_reader = pandas.read_csv(file)
            file_duplicate = file_reader.drop_duplicates() if file_reader.duplicated().sum() != 0 else file_reader
            file_reader = file_duplicate
        return

    def check_missing_rows(self):
        for file in self.trad_team_path.iterdir():
            file_reader = pandas.read_csv(file)
            for items in range(0, len(self.team_identifiers)):
                if file_reader[self.team_identifiers[items]].isna().any():
                    print(f"{self.team_identifiers[items]} is missing in Traditional Team")

        for file in self.adv_team_path.iterdir():
            file_reader = pandas.read_csv(file)
            for items in range(0, len(self.team_identifiers)):
                if file_reader[self.team_identifiers[items]].isna().any():
                    print(f"{self.team_identifiers[items]} is missing in Advanced Team")

        for file in self.trad_player_path.iterdir():
            file_reader = pandas.read_csv(file)
            for items in range(0, len(self.player_identifiers)):
                if file_reader[self.player_identifiers[items]].isna().any():
                    print(f"{self.player_identifiers[items]} is missing in Traditional Players")
        
        for file in self.adv_player_path.iterdir():
            file_reader = pandas.read_csv(file)
            for items in range(0, len(self.player_identifiers)):
                if file_reader[self.player_identifiers[items]].isna().any():
                    print(f"{self.player_identifiers[items]} is missing in Advanced Players")

    def take_out_rank(self):
        for file in self.trad_team_path.iterdir():
            file_reader = pandas.read_csv(file)
            file_rank = [column for column in file_reader.columns if column.endswith("_RANK")]
            file_reader.drop(columns = file_rank, inplace = True)

        for file in self.adv_team_path.iterdir():
            file_reader = pandas.read_csv(file)
            file_rank = [column for column in file_reader.columns if column.endswith("_RANK")]
            file_reader.drop(columns = file_rank, inplace = True)

        for file in self.trad_player_path.iterdir():
            file_reader = pandas.read_csv(file)
            file_rank = [column for column in file_reader.columns if column.endswith("_RANK")]
            file_reader.drop(columns = file_rank, inplace = True)

        for file in self.adv_player_path.iterdir():
            file_reader = pandas.read_csv(file)
            file_rank = [column for column in file_reader.columns if column.endswith("_RANK")]
            file_reader.drop(columns = file_rank, inplace = True)

    def data_filter(self):
        self.season_adder()
        self.check_duplicate_rows()
        self.check_missing_rows()
        self.take_out_rank()

filter = DataFilter()
filter.data_filter()