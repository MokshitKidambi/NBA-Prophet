from pathlib import Path
import pandas
from datetime import date

class UnfilteredDataChecker:
    def __init__(self):
        self.trad_team_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\traditional")
        self.trad_player_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\traditional")
        self.adv_team_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\teams\\advanced")
        self.adv_player_path = Path("C:\\Users\\kidam\\OneDrive\\Documents\\pythonstuff\\NBA-Prophet\\gear3\\data\\unfiltered\\players\\advanced")

        self.trad_team_checker = True
        self.trad_player_checker = True
        self.adv_team_checker = True
        self.adv_player_checker = True
        self.fl_checker = True
        self.col_checker = True
        self.san_checker = True

        self.summary = True


    def traditional_checker(self):
        i = 1996
        j = (i + 1) % 100
        k = 0

        for file in self.trad_team_path.iterdir():
            if i == date.today().year():
                i = 1996
                j = (i + 1) % 100
                k = 0
                break
            if file.name == f"{i}-{j:02d}_traditional_stats.csv":
                i += 1
                k += 1
                j = (i + 1) % 100
                continue
            else:
                self.trad_team_checker = False
                print(f"Team File: {i}-{j:02d}_traditional_stats.csv does not exist")
                continue
        print(f"Team traditional files are good. Count: {k}")

        for file in self.trad_player_path.iterdir():
                    if i == date.today().year():
                         i = 1996
                         j = (i + 1) % 100
                         k = 0
                         break
                    if file.name == f"{i}-{j:02d}_traditional_stats.csv":
                        i += 1
                        k += 1
                        j = (i + 1) % 100
                        continue
                    else:
                        self.trad_player_checker = False
                        print(f"Player File: {i}-{j:02d}_traditional_stats.csv does not exist")
                        continue
        print(f"Player traditional files are good. Count: {k}")

    def advanced_checker(self):
            i = 1996
            j = (i + 1) % 100
            l = 0
    
            for file in self.adv_team_path.iterdir():
                if i == date.today().year():
                    i = 1996
                    j = (i + 1) % 100
                    l = 0
                    break
                if file.name == f"{i}-{j:02d}_advanced_stats.csv":
                    i += 1
                    l += 1
                    j = (i + 1) % 100
                    continue
                else:
                    self.adv_team_checker = False
                    print(f"Team File: {i}-{j:02d}_advanced_stats.csv does not exist")
                    continue
            if self.adv_team_checker == True:
                print(f"Team Advanced files are good. Count: {l}")
            else:
                print("Team Advanced files are not good")

            for file in self.adv_player_path.iterdir():
                        if i == date.today().year():
                             i = 1996
                             j = (i + 1) % 100
                             l = 0
                             break
                        if file.name == f"{i}-{j:02d}_advanced_stats.csv":
                            i+=1
                            j = (i + 1) % 100
                            continue
                        else:
                            self.adv_player_checker = False
                            print(f"Player File: {i}-{j:02d}_advanced_stats.csv does not exist")
                            continue
            if self.adv_player_checker == True:
                print(f"Player Advanced files are good. Count: {l}")
            else:
                 print("Player Advanced files are not good")

    def file_checker(self):
         for file in self.trad_team_path.iterdir():
              if pandas.read_csv(file).empty or pandas.read_csv(file).shape[0] < 1 or pandas.read_csv(file).shape[1] < 1:
                print(f"{file.name} is incomplete")
                self.fl_checker = False
                continue

         for file in self.trad_player_path.iterdir():
              if pandas.read_csv(file).empty or pandas.read_csv(file).shape[0] < 1 or pandas.read_csv(file).shape[1] < 1:
                   print(f"{file.name} is incomplete")
                   self.fl_checker = False
                   continue

         for file in self.trad_team_path.iterdir():
              if pandas.read_csv(file).empty or pandas.read_csv(file).shape[0] < 1 or pandas.read_csv(file).shape[1] < 1:
                   print(f"{file.name} is incomplete")
                   self.fl_checker = False
                   continue
         
         for file in self.trad_player_path.iterdir():
              if pandas.read_csv(file).empty or pandas.read_csv(file).shape[0] < 1 or pandas.read_csv(file).shape[1] < 1:
                   print(f"{file.name} is incomplete")
                   self.fl_checker = False
                   continue

         if self.fl_checker == True: 
            print("File Checker: All files are good")
         else:
              print("File Checker: Some files are faulty")

    def column_checker(self):
         player_column = {"PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "GP"}
         team_column = {"TEAM_ID", "TEAM_NAME", "GP"}

         for file in self.trad_team_path.iterdir():
            datafile = pandas.read_csv(file)
            data_columns = set(datafile.columns)
            if team_column.issubset(data_columns):
                continue
            else:
                 self.col_checker = False
                 print(f"{team_column} does not exist in {file.name}")

         for file in self.trad_player_path.iterdir():
            datafile = pandas.read_csv(file)
            data_columns = set(datafile.columns)
            if player_column.issubset(data_columns):
                continue
            else:
                self.col_checker = False
                print(f"{player_column} does not exist in {file.name}")

         for file in self.adv_team_path.iterdir():
            datafile = pandas.read_csv(file)
            data_columns = set(datafile.columns)
            if team_column.issubset(data_columns):
                continue
            else:
                self.col_checker = False
                print(f"{team_column} does not exist in {file.name}")

         for file in self.adv_player_path.iterdir():
            datafile = pandas.read_csv(file)
            data_columns = set(datafile.columns)
            if player_column.issubset(data_columns):
                continue
            else:
                self.col_checker = False
                print(f"{player_column} does not exist in {file.name}")

         if self.col_checker == True:
              print("Column Checker: Good to Go")
         else:
              print("Column Checker: Faulty Files Found")   

    def sanity_checker(self):
         for file in self.trad_team_path.iterdir():
              datafile = pandas.read_csv(file)
              if (datafile["GP"] > 0).any() == True:
                   if datafile["TEAM_ID"].isna().any() == False:
                        if datafile["TEAM_NAME"].isna().any() == False:
                            if datafile["TEAM_ID"].duplicated().any() == False:
                                 continue
              else:
                   self.san_checker = False
                   print(f"{file.name} does not pass the sanity check")
         for file in self.trad_player_path.iterdir():
              datafile = pandas.read_csv(file)
              if (datafile["GP"] >= 0).any() == True:
                   if datafile["PLAYER_ID"].isna().any() == False:
                        if datafile["PLAYER_NAME"].isna().any() == False:
                             if datafile["PLAYER_ID"].duplicated().any() == False:
                                  continue
              else:
                   self.san_checker = False
                   print(f"{file.name} does not pass the sanity check")
         for file in self.adv_team_path.iterdir():
              datafile = pandas.read_csv(file)
              if (datafile["GP"] > 0).any() == True:
                   if datafile["TEAM_ID"].isna().any() == False:
                        if datafile["TEAM_NAME"].isna().any() == False:
                             if datafile["TEAM_ID"].duplicated().any() == False:
                                  continue
              else:
                   self.san_checker = False
                   print(f"{file.name} does not pass the sanity check")
         for file in self.adv_player_path.iterdir():
              datafile = pandas.read_csv(file)
              if (datafile["GP"] >= 0).any() == True:
                   if datafile["PLAYER_ID"].isna().any() == False:
                        if datafile["PLAYER_NAME"].isna().any() == False:
                             if datafile["PLAYER_ID"].duplicated().any() == False:
                                  continue
              else:
                   self.san_checker = False
                   print(f"{file.name} does not pass the sanity check")

         if self.san_checker == True:
              print("Sanity Checker: Everything is good")
         else:
              print("Sanity Checker: Not all files are good")

    def summary_runner(self):
        print("_____DATA CHECKER SUMMARY:_____")
        print()

        if self.trad_team_checker:
            if self.trad_player_checker:
                print("TRADITIONAL CHECKER: CHECK")
        else:
            self.summary = False
            print("TRADITIONAL CHECKER: NO")

        if self.adv_team_checker:
            if self.adv_player_checker:
                print("ADVANCED CHECKER: CHECK")
        else:
            self.summary = False
            print("ADVANCED CHECKER: NO")

        if self.fl_checker:
            print("FILE CHECKER: CHECK")
        else:
            self.summary = False
            print("FILE CHECKER: NO")

        if self.col_checker:
            print("COLUMN CHECKER: CHECK")
        else:
            self.summary = False
            print("COLUMN CHECKER: NO")

        if self.san_checker:
            print("SANTIY CHECKER: CHECK")
        else:
            self.summary = False
            print("SANITY CHECKER: NO")

        if self.trad_team_checker:
             if self.trad_player_checker:
                  if self.adv_team_checker:
                       if self.adv_player_checker:
                            if self.fl_checker:
                                 if self.san_checker:
                                    print()
                                    print("OVERALL CHECK: GOOD TO GO")
        else:
             self.summary = False
             print()
             print("OVERALL CHECK: STILL NEEDS CHECKS")

    def back_runner(self):
        if self.summary == True:
             return
        else:
            print()
            print()
            print()
            print("_____WHAT WENT WRONG____")
            if self.trad_team_checker == False:
                self.traditional_checker()
                if self.trad_player_checker == False:
                    self.traditional_checker()
                    if self.adv_team_checker == False:
                        self.advanced_checker()
                        if self.adv_player_checker == False:
                            self.advanced_checker()
                            if self.fl_checker == False:
                                self.file_checker()
                                if self.san_checker == False:
                                    self.sanity_checker()

    def runner(self):
         self.summary_runner()
         self.back_runner()
                

