import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

class TranslatingStats:
    def __init__(self):
        self.ncaa_translation_path = Path("ncaa_translation_sample.csv")
        
        self.MPG_X = ["PRE_NBA_MPG"]
        self.MPG_Y = ["FIRST_VALUABLE_NBA_MPG"]
        
        self.PPG_X = ["PRE_NBA_PPG"]
        self.PPG_Y = ["FIRST_VALUABLE_NBA_PPG"]
        
        self.RPG_X = ["PRE_NBA_RPG"]
        self.RPG_Y = ["FIRST_VALUABLE_NBA_RPG"]
                
        self.APG_X = ["PRE_NBA_APG"]
        self.APG_Y = ["FIRST_VALUABLE_NBA_APG"]
                        
        self.TS_PCT_X = ["PRE_NBA_TS_PCT"]
        self.TS_PCT_Y = ["FIRST_VALUABLE_NBA_TS_PCT"]
                                
        self.USG_PCT_X = ["PRE_NBA_USG_PCT"]
        self.USG_PCT_Y = ["FIRST_VALUABLE_NBA_USG_PCT"]
    
    def _2018_stats(self):
                matched = pd.read_csv(self.ncaa_translation_path) 
                
                season_data = matched["DRAFT_YEAR"]
                
                train_mask = season_data.isin([2019, 2020])
                test_mask = season_data == 2018
        
                MPG_X_data = matched[self.MPG_X]
                MPG_Y_data = matched[self.MPG_Y]
                MPG_X_train = MPG_X_data[train_mask]
                MPG_Y_train = MPG_Y_data[train_mask]
                MPG_X_test = MPG_X_data[test_mask]
                MPG_Y_test = MPG_Y_data[test_mask]
                MPG_model = LinearRegression() 
                MPG_model.fit(MPG_X_train, MPG_Y_train)
                
                PPG_X_data = matched[self.PPG_X]
                PPG_Y_data = matched[self.PPG_Y]
        
                
                PPG_X_train = PPG_X_data[train_mask]
                PPG_Y_train = PPG_Y_data[train_mask]
                PPG_X_test = PPG_X_data[test_mask]
                PPG_Y_test = PPG_Y_data[test_mask]
                PPG_model = LinearRegression() 
                PPG_model.fit(PPG_X_train, PPG_Y_train)
                
                RPG_X_data = matched[self.RPG_X]
                RPG_Y_data = matched[self.RPG_Y]
        
                RPG_X_train = RPG_X_data[train_mask]
                RPG_Y_train = RPG_Y_data[train_mask]
                RPG_X_test = RPG_X_data[test_mask]
                RPG_Y_test = RPG_Y_data[test_mask]
                RPG_model = LinearRegression() 
                RPG_model.fit(RPG_X_train, RPG_Y_train)
                
                APG_X_data = matched[self.APG_X]
                APG_Y_data = matched[self.APG_Y]
        
                
                APG_X_train = APG_X_data[train_mask]
                APG_Y_train = APG_Y_data[train_mask]
                APG_X_test = APG_X_data[test_mask]
                APG_Y_test = APG_Y_data[test_mask]
                APG_model = LinearRegression() 
                APG_model.fit(APG_X_train, APG_Y_train)
                
                TS_PCT_X_data = matched[self.TS_PCT_X]
                TS_PCT_Y_data = matched[self.TS_PCT_Y]
        
                
                TS_PCT_X_train = TS_PCT_X_data[train_mask]
                TS_PCT_Y_train = TS_PCT_Y_data[train_mask]
                TS_PCT_X_test = TS_PCT_X_data[test_mask]
                TS_PCT_Y_test = TS_PCT_Y_data[test_mask]
                TS_PCT_model = LinearRegression() 
                TS_PCT_model.fit(TS_PCT_X_train, TS_PCT_Y_train)
                
                USG_PCT_X_data = matched[self.USG_PCT_X]
                USG_PCT_Y_data = matched[self.USG_PCT_Y]
        
                
                USG_PCT_X_train = USG_PCT_X_data[train_mask]
                USG_PCT_Y_train = USG_PCT_Y_data[train_mask]
                USG_PCT_X_test = USG_PCT_X_data[test_mask]
                USG_PCT_Y_test = USG_PCT_Y_data[test_mask]
                USG_PCT_model = LinearRegression() 
                USG_PCT_model.fit(USG_PCT_X_train, USG_PCT_Y_train)
                
                test_info = matched.loc[test_mask, ["PLAYER_ID", "PLAYER_NAME", "DRAFT_YEAR"]].copy()
                
                MPG_prediction = MPG_model.predict(MPG_X_test).ravel()
                PPG_prediction = PPG_model.predict(PPG_X_test).ravel()
                RPG_prediction = RPG_model.predict(RPG_X_test).ravel()
                APG_prediction = APG_model.predict(APG_X_test).ravel()
                TS_PCT_prediction = TS_PCT_model.predict(TS_PCT_X_test).ravel()
                USG_PCT_prediction = USG_PCT_model.predict(USG_PCT_X_test).ravel()
                
                MPG_mae = mean_absolute_error(MPG_Y_test, MPG_prediction)
                PPG_mae = mean_absolute_error(PPG_Y_test, PPG_prediction)
                RPG_mae = mean_absolute_error(RPG_Y_test, RPG_prediction)
                APG_mae = mean_absolute_error(APG_Y_test, APG_prediction)
                TS_PCT_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_prediction)
                USG_PCT_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_prediction)
                
                MPG_result = pd.DataFrame()
                         
                MPG_result["ACTUAL_NBA_STAT"] = MPG_Y_test
                MPG_result["PREDICTED_NBA_STAT"] = MPG_prediction
                MPG_result["MAE"] = MPG_mae
                
                PPG_result = pd.DataFrame()
                         
                PPG_result["ACTUAL_NBA_STAT"] = PPG_Y_test
                PPG_result["PREDICTED_NBA_STAT"] = PPG_prediction
                PPG_result["MAE"] = PPG_mae
                
                RPG_result = pd.DataFrame()
                         
                RPG_result["ACTUAL_NBA_STAT"] = RPG_Y_test
                RPG_result["PREDICTED_NBA_STAT"] = RPG_prediction
                RPG_result["MAE"] = RPG_mae
                
                APG_result = pd.DataFrame()
                         
                APG_result["ACTUAL_NBA_STAT"] = APG_Y_test
                APG_result["PREDICTED_NBA_STAT"] = APG_prediction
                APG_result["MAE"] = APG_mae
                
                TS_PCT_result = pd.DataFrame()
                
                TS_PCT_result["ACTUAL_NBA_STAT"] = TS_PCT_Y_test
                TS_PCT_result["PREDICTED_NBA_STAT"] = TS_PCT_prediction
                TS_PCT_result["MAE"] = TS_PCT_mae
                
                USG_PCT_result = pd.DataFrame()
                
                USG_PCT_result["ACTUAL_NBA_STAT"] = USG_PCT_Y_test
                USG_PCT_result["PREDICTED_NBA_STAT"] = USG_PCT_prediction
                USG_PCT_result["MAE"] = USG_PCT_mae
                
                MPG_naive_value = MPG_Y_train.iloc[:, 0].mean()
                MPG_naive_prediction = np.full(len(MPG_Y_test), MPG_naive_value)
                MPG_naive_mae = mean_absolute_error(MPG_Y_test, MPG_naive_prediction)
        
        
                PPG_naive_value = PPG_Y_train.iloc[:, 0].mean()
                PPG_naive_prediction = np.full(len(PPG_Y_test), PPG_naive_value)
                PPG_naive_mae = mean_absolute_error(PPG_Y_test, PPG_naive_prediction)
        
        
                RPG_naive_value = RPG_Y_train.iloc[:, 0].mean()
                RPG_naive_prediction = np.full(len(RPG_Y_test), RPG_naive_value)
                RPG_naive_mae = mean_absolute_error(RPG_Y_test, RPG_naive_prediction)
        
        
                APG_naive_value = APG_Y_train.iloc[:, 0].mean()
                APG_naive_prediction = np.full(len(APG_Y_test), APG_naive_value)
                APG_naive_mae = mean_absolute_error(APG_Y_test, APG_naive_prediction)
        
        
                TS_PCT_naive_value = TS_PCT_Y_train.iloc[:, 0].mean()
                TS_PCT_naive_prediction = np.full(len(TS_PCT_Y_test), TS_PCT_naive_value)
                TS_PCT_naive_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_naive_prediction)
        
                USG_PCT_naive_value = USG_PCT_Y_train.iloc[:, 0].mean()
                USG_PCT_naive_prediction = np.full(len(USG_PCT_Y_test), USG_PCT_naive_value)
                USG_PCT_naive_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_naive_prediction)
                
                MPG_ratio = (MPG_Y_train.iloc[:, 0].mean()/ MPG_X_train.iloc[:, 0].mean())
                MPG_ratio_prediction = (MPG_X_test.iloc[:, 0] * MPG_ratio)
                MPG_ratio_mae = mean_absolute_error(MPG_Y_test, MPG_ratio_prediction)
    
                PPG_ratio = (PPG_Y_train.iloc[:, 0].mean()/ PPG_X_train.iloc[:, 0].mean())
                PPG_ratio_prediction = (PPG_X_test.iloc[:, 0] * PPG_ratio)
                PPG_ratio_mae = mean_absolute_error(PPG_Y_test, PPG_ratio_prediction)
                
                RPG_ratio = (RPG_Y_train.iloc[:, 0].mean()/ RPG_X_train.iloc[:, 0].mean())
                RPG_ratio_prediction = (RPG_X_test.iloc[:, 0] * RPG_ratio)
                RPG_ratio_mae = mean_absolute_error(RPG_Y_test, RPG_ratio_prediction)
                
                APG_ratio = (APG_Y_train.iloc[:, 0].mean()/ APG_X_train.iloc[:, 0].mean())
                APG_ratio_prediction = (APG_X_test.iloc[:, 0] * APG_ratio)
                APG_ratio_mae = mean_absolute_error(APG_Y_test, APG_ratio_prediction)
                
                TS_PCT_ratio = (TS_PCT_Y_train.iloc[:, 0].mean()/ TS_PCT_X_train.iloc[:, 0].mean())
                TS_PCT_ratio_prediction = (TS_PCT_X_test.iloc[:, 0] * TS_PCT_ratio)
                TS_PCT_ratio_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_ratio_prediction)
                
                USG_PCT_ratio = (USG_PCT_Y_train.iloc[:, 0].mean()/ USG_PCT_X_train.iloc[:, 0].mean())
                USG_PCT_ratio_prediction = (USG_PCT_X_test.iloc[:, 0] * USG_PCT_ratio)
                USG_PCT_ratio_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_ratio_prediction)
                
                
                print("MPG REGRESSION MAE:", round(MPG_mae, 3))
                print("PPG REGRESSION MAE:", round(PPG_mae, 3))
                print("RPG REGRESSION MAE:", round(RPG_mae, 3))
                print("APG REGRESSION MAE:", round(APG_mae, 3))
                print("TS_PCT REGRESSION MAE:", round(TS_PCT_mae, 3))
                print("USG_PCT REGRESSION MAE:", round(USG_PCT_mae, 3))
                print()
                print("MPG NAIVE MAE:", round(MPG_naive_mae, 3))
                print("PPG NAIVE MAE:", round(PPG_naive_mae, 3))
                print("RPG NAIVE MAE:", round(RPG_naive_mae, 3))
                print("APG NAIVE MAE:", round(APG_naive_mae, 3))
                print("TS_PCT NAIVE MAE:", round(TS_PCT_naive_mae, 3))
                print("USG_PCT NAIVE MAE:", round(USG_PCT_naive_mae, 3))
                print()
                print("MPG RATIO MAE:", round(MPG_ratio_mae, 3))
                print("PPG RATIO MAE:", round(PPG_ratio_mae, 3))
                print("RPG RATIO MAE:", round(RPG_ratio_mae, 3))
                print("APG RATIO MAE:", round(APG_ratio_mae, 3))
                print("TS_PCT RATIO MAE:", round(TS_PCT_ratio_mae, 3))
                print("USG_PCT RATIO MAE:", round(USG_PCT_ratio_mae, 3))
    
    def _2019_stats(self):
                matched = pd.read_csv(self.ncaa_translation_path) 
                
                season_data = matched["DRAFT_YEAR"]
                
                train_mask = season_data.isin([2018, 2020])
                test_mask = season_data == 2019
        
                MPG_X_data = matched[self.MPG_X]
                MPG_Y_data = matched[self.MPG_Y]
                MPG_X_train = MPG_X_data[train_mask]
                MPG_Y_train = MPG_Y_data[train_mask]
                MPG_X_test = MPG_X_data[test_mask]
                MPG_Y_test = MPG_Y_data[test_mask]
                MPG_model = LinearRegression() 
                MPG_model.fit(MPG_X_train, MPG_Y_train)
                
                PPG_X_data = matched[self.PPG_X]
                PPG_Y_data = matched[self.PPG_Y]
        
                
                PPG_X_train = PPG_X_data[train_mask]
                PPG_Y_train = PPG_Y_data[train_mask]
                PPG_X_test = PPG_X_data[test_mask]
                PPG_Y_test = PPG_Y_data[test_mask]
                PPG_model = LinearRegression() 
                PPG_model.fit(PPG_X_train, PPG_Y_train)
                
                RPG_X_data = matched[self.RPG_X]
                RPG_Y_data = matched[self.RPG_Y]
        
                RPG_X_train = RPG_X_data[train_mask]
                RPG_Y_train = RPG_Y_data[train_mask]
                RPG_X_test = RPG_X_data[test_mask]
                RPG_Y_test = RPG_Y_data[test_mask]
                RPG_model = LinearRegression() 
                RPG_model.fit(RPG_X_train, RPG_Y_train)
                
                APG_X_data = matched[self.APG_X]
                APG_Y_data = matched[self.APG_Y]
        
                
                APG_X_train = APG_X_data[train_mask]
                APG_Y_train = APG_Y_data[train_mask]
                APG_X_test = APG_X_data[test_mask]
                APG_Y_test = APG_Y_data[test_mask]
                APG_model = LinearRegression() 
                APG_model.fit(APG_X_train, APG_Y_train)
                
                TS_PCT_X_data = matched[self.TS_PCT_X]
                TS_PCT_Y_data = matched[self.TS_PCT_Y]
        
                
                TS_PCT_X_train = TS_PCT_X_data[train_mask]
                TS_PCT_Y_train = TS_PCT_Y_data[train_mask]
                TS_PCT_X_test = TS_PCT_X_data[test_mask]
                TS_PCT_Y_test = TS_PCT_Y_data[test_mask]
                TS_PCT_model = LinearRegression() 
                TS_PCT_model.fit(TS_PCT_X_train, TS_PCT_Y_train)
                
                USG_PCT_X_data = matched[self.USG_PCT_X]
                USG_PCT_Y_data = matched[self.USG_PCT_Y]
        
                
                USG_PCT_X_train = USG_PCT_X_data[train_mask]
                USG_PCT_Y_train = USG_PCT_Y_data[train_mask]
                USG_PCT_X_test = USG_PCT_X_data[test_mask]
                USG_PCT_Y_test = USG_PCT_Y_data[test_mask]
                USG_PCT_model = LinearRegression() 
                USG_PCT_model.fit(USG_PCT_X_train, USG_PCT_Y_train)
                
                test_info = matched.loc[test_mask, ["PLAYER_ID", "PLAYER_NAME", "DRAFT_YEAR"]].copy()
                
                MPG_prediction = MPG_model.predict(MPG_X_test).ravel()
                PPG_prediction = PPG_model.predict(PPG_X_test).ravel()
                RPG_prediction = RPG_model.predict(RPG_X_test).ravel()
                APG_prediction = APG_model.predict(APG_X_test).ravel()
                TS_PCT_prediction = TS_PCT_model.predict(TS_PCT_X_test).ravel()
                USG_PCT_prediction = USG_PCT_model.predict(USG_PCT_X_test).ravel()
                
                MPG_mae = mean_absolute_error(MPG_Y_test, MPG_prediction)
                PPG_mae = mean_absolute_error(PPG_Y_test, PPG_prediction)
                RPG_mae = mean_absolute_error(RPG_Y_test, RPG_prediction)
                APG_mae = mean_absolute_error(APG_Y_test, APG_prediction)
                TS_PCT_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_prediction)
                USG_PCT_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_prediction)
                
                MPG_result = pd.DataFrame()
                         
                MPG_result["ACTUAL_NBA_STAT"] = MPG_Y_test
                MPG_result["PREDICTED_NBA_STAT"] = MPG_prediction
                MPG_result["MAE"] = MPG_mae
                
                PPG_result = pd.DataFrame()
                         
                PPG_result["ACTUAL_NBA_STAT"] = PPG_Y_test
                PPG_result["PREDICTED_NBA_STAT"] = PPG_prediction
                PPG_result["MAE"] = PPG_mae
                
                RPG_result = pd.DataFrame()
                         
                RPG_result["ACTUAL_NBA_STAT"] = RPG_Y_test
                RPG_result["PREDICTED_NBA_STAT"] = RPG_prediction
                RPG_result["MAE"] = RPG_mae
                
                APG_result = pd.DataFrame()
                         
                APG_result["ACTUAL_NBA_STAT"] = APG_Y_test
                APG_result["PREDICTED_NBA_STAT"] = APG_prediction
                APG_result["MAE"] = APG_mae
                
                TS_PCT_result = pd.DataFrame()
                
                TS_PCT_result["ACTUAL_NBA_STAT"] = TS_PCT_Y_test
                TS_PCT_result["PREDICTED_NBA_STAT"] = TS_PCT_prediction
                TS_PCT_result["MAE"] = TS_PCT_mae
                
                USG_PCT_result = pd.DataFrame()
                
                USG_PCT_result["ACTUAL_NBA_STAT"] = USG_PCT_Y_test
                USG_PCT_result["PREDICTED_NBA_STAT"] = USG_PCT_prediction
                USG_PCT_result["MAE"] = USG_PCT_mae
                
                MPG_naive_value = MPG_Y_train.iloc[:, 0].mean()
                MPG_naive_prediction = np.full(len(MPG_Y_test), MPG_naive_value)
                MPG_naive_mae = mean_absolute_error(MPG_Y_test, MPG_naive_prediction)
        
        
                PPG_naive_value = PPG_Y_train.iloc[:, 0].mean()
                PPG_naive_prediction = np.full(len(PPG_Y_test), PPG_naive_value)
                PPG_naive_mae = mean_absolute_error(PPG_Y_test, PPG_naive_prediction)
        
        
                RPG_naive_value = RPG_Y_train.iloc[:, 0].mean()
                RPG_naive_prediction = np.full(len(RPG_Y_test), RPG_naive_value)
                RPG_naive_mae = mean_absolute_error(RPG_Y_test, RPG_naive_prediction)
        
        
                APG_naive_value = APG_Y_train.iloc[:, 0].mean()
                APG_naive_prediction = np.full(len(APG_Y_test), APG_naive_value)
                APG_naive_mae = mean_absolute_error(APG_Y_test, APG_naive_prediction)
        
        
                TS_PCT_naive_value = TS_PCT_Y_train.iloc[:, 0].mean()
                TS_PCT_naive_prediction = np.full(len(TS_PCT_Y_test), TS_PCT_naive_value)
                TS_PCT_naive_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_naive_prediction)
        
                USG_PCT_naive_value = USG_PCT_Y_train.iloc[:, 0].mean()
                USG_PCT_naive_prediction = np.full(len(USG_PCT_Y_test), USG_PCT_naive_value)
                USG_PCT_naive_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_naive_prediction)
                
                MPG_ratio = (MPG_Y_train.iloc[:, 0].mean()/ MPG_X_train.iloc[:, 0].mean())
                MPG_ratio_prediction = (MPG_X_test.iloc[:, 0] * MPG_ratio)
                MPG_ratio_mae = mean_absolute_error(MPG_Y_test, MPG_ratio_prediction)
    
                PPG_ratio = (PPG_Y_train.iloc[:, 0].mean()/ PPG_X_train.iloc[:, 0].mean())
                PPG_ratio_prediction = (PPG_X_test.iloc[:, 0] * PPG_ratio)
                PPG_ratio_mae = mean_absolute_error(PPG_Y_test, PPG_ratio_prediction)
                
                RPG_ratio = (RPG_Y_train.iloc[:, 0].mean()/ RPG_X_train.iloc[:, 0].mean())
                RPG_ratio_prediction = (RPG_X_test.iloc[:, 0] * RPG_ratio)
                RPG_ratio_mae = mean_absolute_error(RPG_Y_test, RPG_ratio_prediction)
                
                APG_ratio = (APG_Y_train.iloc[:, 0].mean()/ APG_X_train.iloc[:, 0].mean())
                APG_ratio_prediction = (APG_X_test.iloc[:, 0] * APG_ratio)
                APG_ratio_mae = mean_absolute_error(APG_Y_test, APG_ratio_prediction)
                
                TS_PCT_ratio = (TS_PCT_Y_train.iloc[:, 0].mean()/ TS_PCT_X_train.iloc[:, 0].mean())
                TS_PCT_ratio_prediction = (TS_PCT_X_test.iloc[:, 0] * TS_PCT_ratio)
                TS_PCT_ratio_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_ratio_prediction)
                
                USG_PCT_ratio = (USG_PCT_Y_train.iloc[:, 0].mean()/ USG_PCT_X_train.iloc[:, 0].mean())
                USG_PCT_ratio_prediction = (USG_PCT_X_test.iloc[:, 0] * USG_PCT_ratio)
                USG_PCT_ratio_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_ratio_prediction)
                
                
                print("MPG REGRESSION MAE:", round(MPG_mae, 3))
                print("PPG REGRESSION MAE:", round(PPG_mae, 3))
                print("RPG REGRESSION MAE:", round(RPG_mae, 3))
                print("APG REGRESSION MAE:", round(APG_mae, 3))
                print("TS_PCT REGRESSION MAE:", round(TS_PCT_mae, 3))
                print("USG_PCT REGRESSION MAE:", round(USG_PCT_mae, 3))
                print()
                print("MPG NAIVE MAE:", round(MPG_naive_mae, 3))
                print("PPG NAIVE MAE:", round(PPG_naive_mae, 3))
                print("RPG NAIVE MAE:", round(RPG_naive_mae, 3))
                print("APG NAIVE MAE:", round(APG_naive_mae, 3))
                print("TS_PCT NAIVE MAE:", round(TS_PCT_naive_mae, 3))
                print("USG_PCT NAIVE MAE:", round(USG_PCT_naive_mae, 3))
                print()
                print("MPG RATIO MAE:", round(MPG_ratio_mae, 3))
                print("PPG RATIO MAE:", round(PPG_ratio_mae, 3))
                print("RPG RATIO MAE:", round(RPG_ratio_mae, 3))
                print("APG RATIO MAE:", round(APG_ratio_mae, 3))
                print("TS_PCT RATIO MAE:", round(TS_PCT_ratio_mae, 3))
                print("USG_PCT RATIO MAE:", round(USG_PCT_ratio_mae, 3))
    
    def _2020_stats(self):
            matched = pd.read_csv(self.ncaa_translation_path) 
            
            season_data = matched["DRAFT_YEAR"]
            
            train_mask = season_data.isin([2018, 2019])
            test_mask = season_data == 2020
    
            MPG_X_data = matched[self.MPG_X]
            MPG_Y_data = matched[self.MPG_Y]
            MPG_X_train = MPG_X_data[train_mask]
            MPG_Y_train = MPG_Y_data[train_mask]
            MPG_X_test = MPG_X_data[test_mask]
            MPG_Y_test = MPG_Y_data[test_mask]
            MPG_model = LinearRegression() 
            MPG_model.fit(MPG_X_train, MPG_Y_train)
            
            PPG_X_data = matched[self.PPG_X]
            PPG_Y_data = matched[self.PPG_Y]
    
            
            PPG_X_train = PPG_X_data[train_mask]
            PPG_Y_train = PPG_Y_data[train_mask]
            PPG_X_test = PPG_X_data[test_mask]
            PPG_Y_test = PPG_Y_data[test_mask]
            PPG_model = LinearRegression() 
            PPG_model.fit(PPG_X_train, PPG_Y_train)
            
            RPG_X_data = matched[self.RPG_X]
            RPG_Y_data = matched[self.RPG_Y]
    
            RPG_X_train = RPG_X_data[train_mask]
            RPG_Y_train = RPG_Y_data[train_mask]
            RPG_X_test = RPG_X_data[test_mask]
            RPG_Y_test = RPG_Y_data[test_mask]
            RPG_model = LinearRegression() 
            RPG_model.fit(RPG_X_train, RPG_Y_train)
            
            APG_X_data = matched[self.APG_X]
            APG_Y_data = matched[self.APG_Y]
    
            
            APG_X_train = APG_X_data[train_mask]
            APG_Y_train = APG_Y_data[train_mask]
            APG_X_test = APG_X_data[test_mask]
            APG_Y_test = APG_Y_data[test_mask]
            APG_model = LinearRegression() 
            APG_model.fit(APG_X_train, APG_Y_train)
            
            TS_PCT_X_data = matched[self.TS_PCT_X]
            TS_PCT_Y_data = matched[self.TS_PCT_Y]
    
            
            TS_PCT_X_train = TS_PCT_X_data[train_mask]
            TS_PCT_Y_train = TS_PCT_Y_data[train_mask]
            TS_PCT_X_test = TS_PCT_X_data[test_mask]
            TS_PCT_Y_test = TS_PCT_Y_data[test_mask]
            TS_PCT_model = LinearRegression() 
            TS_PCT_model.fit(TS_PCT_X_train, TS_PCT_Y_train)
            
            USG_PCT_X_data = matched[self.USG_PCT_X]
            USG_PCT_Y_data = matched[self.USG_PCT_Y]
    
            
            USG_PCT_X_train = USG_PCT_X_data[train_mask]
            USG_PCT_Y_train = USG_PCT_Y_data[train_mask]
            USG_PCT_X_test = USG_PCT_X_data[test_mask]
            USG_PCT_Y_test = USG_PCT_Y_data[test_mask]
            USG_PCT_model = LinearRegression() 
            USG_PCT_model.fit(USG_PCT_X_train, USG_PCT_Y_train)
            
            test_info = matched.loc[test_mask, ["PLAYER_ID", "PLAYER_NAME", "DRAFT_YEAR"]].copy()
            
            MPG_prediction = MPG_model.predict(MPG_X_test).ravel()
            PPG_prediction = PPG_model.predict(PPG_X_test).ravel()
            RPG_prediction = RPG_model.predict(RPG_X_test).ravel()
            APG_prediction = APG_model.predict(APG_X_test).ravel()
            TS_PCT_prediction = TS_PCT_model.predict(TS_PCT_X_test).ravel()
            USG_PCT_prediction = USG_PCT_model.predict(USG_PCT_X_test).ravel()
            
            MPG_mae = mean_absolute_error(MPG_Y_test, MPG_prediction)
            PPG_mae = mean_absolute_error(PPG_Y_test, PPG_prediction)
            RPG_mae = mean_absolute_error(RPG_Y_test, RPG_prediction)
            APG_mae = mean_absolute_error(APG_Y_test, APG_prediction)
            TS_PCT_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_prediction)
            USG_PCT_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_prediction)
            
            MPG_result = pd.DataFrame()
                     
            MPG_result["ACTUAL_NBA_STAT"] = MPG_Y_test
            MPG_result["PREDICTED_NBA_STAT"] = MPG_prediction
            MPG_result["MAE"] = MPG_mae
            
            PPG_result = pd.DataFrame()
                     
            PPG_result["ACTUAL_NBA_STAT"] = PPG_Y_test
            PPG_result["PREDICTED_NBA_STAT"] = PPG_prediction
            PPG_result["MAE"] = PPG_mae
            
            RPG_result = pd.DataFrame()
                     
            RPG_result["ACTUAL_NBA_STAT"] = RPG_Y_test
            RPG_result["PREDICTED_NBA_STAT"] = RPG_prediction
            RPG_result["MAE"] = RPG_mae
            
            APG_result = pd.DataFrame()
                     
            APG_result["ACTUAL_NBA_STAT"] = APG_Y_test
            APG_result["PREDICTED_NBA_STAT"] = APG_prediction
            APG_result["MAE"] = APG_mae
            
            TS_PCT_result = pd.DataFrame()
            
            TS_PCT_result["ACTUAL_NBA_STAT"] = TS_PCT_Y_test
            TS_PCT_result["PREDICTED_NBA_STAT"] = TS_PCT_prediction
            TS_PCT_result["MAE"] = TS_PCT_mae
            
            USG_PCT_result = pd.DataFrame()
            
            USG_PCT_result["ACTUAL_NBA_STAT"] = USG_PCT_Y_test
            USG_PCT_result["PREDICTED_NBA_STAT"] = USG_PCT_prediction
            USG_PCT_result["MAE"] = USG_PCT_mae
            
            MPG_naive_value = MPG_Y_train.iloc[:, 0].mean()
            MPG_naive_prediction = np.full(len(MPG_Y_test), MPG_naive_value)
            MPG_naive_mae = mean_absolute_error(MPG_Y_test, MPG_naive_prediction)
    
    
            PPG_naive_value = PPG_Y_train.iloc[:, 0].mean()
            PPG_naive_prediction = np.full(len(PPG_Y_test), PPG_naive_value)
            PPG_naive_mae = mean_absolute_error(PPG_Y_test, PPG_naive_prediction)
    
    
            RPG_naive_value = RPG_Y_train.iloc[:, 0].mean()
            RPG_naive_prediction = np.full(len(RPG_Y_test), RPG_naive_value)
            RPG_naive_mae = mean_absolute_error(RPG_Y_test, RPG_naive_prediction)
    
    
            APG_naive_value = APG_Y_train.iloc[:, 0].mean()
            APG_naive_prediction = np.full(len(APG_Y_test), APG_naive_value)
            APG_naive_mae = mean_absolute_error(APG_Y_test, APG_naive_prediction)
    
    
            TS_PCT_naive_value = TS_PCT_Y_train.iloc[:, 0].mean()
            TS_PCT_naive_prediction = np.full(len(TS_PCT_Y_test), TS_PCT_naive_value)
            TS_PCT_naive_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_naive_prediction)
    
            USG_PCT_naive_value = USG_PCT_Y_train.iloc[:, 0].mean()
            USG_PCT_naive_prediction = np.full(len(USG_PCT_Y_test), USG_PCT_naive_value)
            USG_PCT_naive_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_naive_prediction)
            
            MPG_ratio = (MPG_Y_train.iloc[:, 0].mean()/ MPG_X_train.iloc[:, 0].mean())
            MPG_ratio_prediction = (MPG_X_test.iloc[:, 0] * MPG_ratio)
            MPG_ratio_mae = mean_absolute_error(MPG_Y_test, MPG_ratio_prediction)

            PPG_ratio = (PPG_Y_train.iloc[:, 0].mean()/ PPG_X_train.iloc[:, 0].mean())
            PPG_ratio_prediction = (PPG_X_test.iloc[:, 0] * PPG_ratio)
            PPG_ratio_mae = mean_absolute_error(PPG_Y_test, PPG_ratio_prediction)
            
            RPG_ratio = (RPG_Y_train.iloc[:, 0].mean()/ RPG_X_train.iloc[:, 0].mean())
            RPG_ratio_prediction = (RPG_X_test.iloc[:, 0] * RPG_ratio)
            RPG_ratio_mae = mean_absolute_error(RPG_Y_test, RPG_ratio_prediction)
            
            APG_ratio = (APG_Y_train.iloc[:, 0].mean()/ APG_X_train.iloc[:, 0].mean())
            APG_ratio_prediction = (APG_X_test.iloc[:, 0] * APG_ratio)
            APG_ratio_mae = mean_absolute_error(APG_Y_test, APG_ratio_prediction)
            
            TS_PCT_ratio = (TS_PCT_Y_train.iloc[:, 0].mean()/ TS_PCT_X_train.iloc[:, 0].mean())
            TS_PCT_ratio_prediction = (TS_PCT_X_test.iloc[:, 0] * TS_PCT_ratio)
            TS_PCT_ratio_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_ratio_prediction)
            
            USG_PCT_ratio = (USG_PCT_Y_train.iloc[:, 0].mean()/ USG_PCT_X_train.iloc[:, 0].mean())
            USG_PCT_ratio_prediction = (USG_PCT_X_test.iloc[:, 0] * USG_PCT_ratio)
            USG_PCT_ratio_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_ratio_prediction)
            
            
            print("MPG REGRESSION MAE:", round(MPG_mae, 3))
            print("PPG REGRESSION MAE:", round(PPG_mae, 3))
            print("RPG REGRESSION MAE:", round(RPG_mae, 3))
            print("APG REGRESSION MAE:", round(APG_mae, 3))
            print("TS_PCT REGRESSION MAE:", round(TS_PCT_mae, 3))
            print("USG_PCT REGRESSION MAE:", round(USG_PCT_mae, 3))
            print()
            print("MPG NAIVE MAE:", round(MPG_naive_mae, 3))
            print("PPG NAIVE MAE:", round(PPG_naive_mae, 3))
            print("RPG NAIVE MAE:", round(RPG_naive_mae, 3))
            print("APG NAIVE MAE:", round(APG_naive_mae, 3))
            print("TS_PCT NAIVE MAE:", round(TS_PCT_naive_mae, 3))
            print("USG_PCT NAIVE MAE:", round(USG_PCT_naive_mae, 3))
            print()
            print("MPG RATIO MAE:", round(MPG_ratio_mae, 3))
            print("PPG RATIO MAE:", round(PPG_ratio_mae, 3))
            print("RPG RATIO MAE:", round(RPG_ratio_mae, 3))
            print("APG RATIO MAE:", round(APG_ratio_mae, 3))
            print("TS_PCT RATIO MAE:", round(TS_PCT_ratio_mae, 3))
            print("USG_PCT RATIO MAE:", round(USG_PCT_ratio_mae, 3))
            
    def _2021_stats(self):
                matched = pd.read_csv(self.ncaa_translation_path) 
                
                season_data = matched["DRAFT_YEAR"]
                
                train_mask = season_data.isin([2018, 2019])
                test_mask = season_data == 2020
        
                MPG_X_data = matched[self.MPG_X]
                MPG_Y_data = matched[self.MPG_Y]
                MPG_X_train = MPG_X_data[train_mask]
                MPG_Y_train = MPG_Y_data[train_mask]
                MPG_X_test = MPG_X_data[test_mask]
                MPG_Y_test = MPG_Y_data[test_mask]
                MPG_model = LinearRegression() 
                MPG_model.fit(MPG_X_train, MPG_Y_train)
                
                PPG_X_data = matched[self.PPG_X]
                PPG_Y_data = matched[self.PPG_Y]
        
                
                PPG_X_train = PPG_X_data[train_mask]
                PPG_Y_train = PPG_Y_data[train_mask]
                PPG_X_test = PPG_X_data[test_mask]
                PPG_Y_test = PPG_Y_data[test_mask]
                PPG_model = LinearRegression() 
                PPG_model.fit(PPG_X_train, PPG_Y_train)
                
                RPG_X_data = matched[self.RPG_X]
                RPG_Y_data = matched[self.RPG_Y]
        
                RPG_X_train = RPG_X_data[train_mask]
                RPG_Y_train = RPG_Y_data[train_mask]
                RPG_X_test = RPG_X_data[test_mask]
                RPG_Y_test = RPG_Y_data[test_mask]
                RPG_model = LinearRegression() 
                RPG_model.fit(RPG_X_train, RPG_Y_train)
                
                APG_X_data = matched[self.APG_X]
                APG_Y_data = matched[self.APG_Y]
        
                
                APG_X_train = APG_X_data[train_mask]
                APG_Y_train = APG_Y_data[train_mask]
                APG_X_test = APG_X_data[test_mask]
                APG_Y_test = APG_Y_data[test_mask]
                APG_model = LinearRegression() 
                APG_model.fit(APG_X_train, APG_Y_train)
                
                TS_PCT_X_data = matched[self.TS_PCT_X]
                TS_PCT_Y_data = matched[self.TS_PCT_Y]
        
                
                TS_PCT_X_train = TS_PCT_X_data[train_mask]
                TS_PCT_Y_train = TS_PCT_Y_data[train_mask]
                TS_PCT_X_test = TS_PCT_X_data[test_mask]
                TS_PCT_Y_test = TS_PCT_Y_data[test_mask]
                TS_PCT_model = LinearRegression() 
                TS_PCT_model.fit(TS_PCT_X_train, TS_PCT_Y_train)
                
                USG_PCT_X_data = matched[self.USG_PCT_X]
                USG_PCT_Y_data = matched[self.USG_PCT_Y]
        
                
                USG_PCT_X_train = USG_PCT_X_data[train_mask]
                USG_PCT_Y_train = USG_PCT_Y_data[train_mask]
                USG_PCT_X_test = USG_PCT_X_data[test_mask]
                USG_PCT_Y_test = USG_PCT_Y_data[test_mask]
                USG_PCT_model = LinearRegression() 
                USG_PCT_model.fit(USG_PCT_X_train, USG_PCT_Y_train)
                
                test_info = matched.loc[test_mask, ["PLAYER_ID", "PLAYER_NAME", "DRAFT_YEAR"]].copy()
                
                MPG_prediction = MPG_model.predict(MPG_X_test).ravel()
                PPG_prediction = PPG_model.predict(PPG_X_test).ravel()
                RPG_prediction = RPG_model.predict(RPG_X_test).ravel()
                APG_prediction = APG_model.predict(APG_X_test).ravel()
                TS_PCT_prediction = TS_PCT_model.predict(TS_PCT_X_test).ravel()
                USG_PCT_prediction = USG_PCT_model.predict(USG_PCT_X_test).ravel()
                
                MPG_mae = mean_absolute_error(MPG_Y_test, MPG_prediction)
                PPG_mae = mean_absolute_error(PPG_Y_test, PPG_prediction)
                RPG_mae = mean_absolute_error(RPG_Y_test, RPG_prediction)
                APG_mae = mean_absolute_error(APG_Y_test, APG_prediction)
                TS_PCT_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_prediction)
                USG_PCT_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_prediction)
                
                MPG_result = pd.DataFrame()
                         
                MPG_result["ACTUAL_NBA_STAT"] = MPG_Y_test
                MPG_result["PREDICTED_NBA_STAT"] = MPG_prediction
                MPG_result["MAE"] = MPG_mae
                
                PPG_result = pd.DataFrame()
                         
                PPG_result["ACTUAL_NBA_STAT"] = PPG_Y_test
                PPG_result["PREDICTED_NBA_STAT"] = PPG_prediction
                PPG_result["MAE"] = PPG_mae
                
                RPG_result = pd.DataFrame()
                         
                RPG_result["ACTUAL_NBA_STAT"] = RPG_Y_test
                RPG_result["PREDICTED_NBA_STAT"] = RPG_prediction
                RPG_result["MAE"] = RPG_mae
                
                APG_result = pd.DataFrame()
                         
                APG_result["ACTUAL_NBA_STAT"] = APG_Y_test
                APG_result["PREDICTED_NBA_STAT"] = APG_prediction
                APG_result["MAE"] = APG_mae
                
                TS_PCT_result = pd.DataFrame()
                
                TS_PCT_result["ACTUAL_NBA_STAT"] = TS_PCT_Y_test
                TS_PCT_result["PREDICTED_NBA_STAT"] = TS_PCT_prediction
                TS_PCT_result["MAE"] = TS_PCT_mae
                
                USG_PCT_result = pd.DataFrame()
                
                USG_PCT_result["ACTUAL_NBA_STAT"] = USG_PCT_Y_test
                USG_PCT_result["PREDICTED_NBA_STAT"] = USG_PCT_prediction
                USG_PCT_result["MAE"] = USG_PCT_mae
                
                MPG_naive_value = MPG_Y_train.iloc[:, 0].mean()
                MPG_naive_prediction = np.full(len(MPG_Y_test), MPG_naive_value)
                MPG_naive_mae = mean_absolute_error(MPG_Y_test, MPG_naive_prediction)
        
        
                PPG_naive_value = PPG_Y_train.iloc[:, 0].mean()
                PPG_naive_prediction = np.full(len(PPG_Y_test), PPG_naive_value)
                PPG_naive_mae = mean_absolute_error(PPG_Y_test, PPG_naive_prediction)
        
        
                RPG_naive_value = RPG_Y_train.iloc[:, 0].mean()
                RPG_naive_prediction = np.full(len(RPG_Y_test), RPG_naive_value)
                RPG_naive_mae = mean_absolute_error(RPG_Y_test, RPG_naive_prediction)
        
        
                APG_naive_value = APG_Y_train.iloc[:, 0].mean()
                APG_naive_prediction = np.full(len(APG_Y_test), APG_naive_value)
                APG_naive_mae = mean_absolute_error(APG_Y_test, APG_naive_prediction)
        
        
                TS_PCT_naive_value = TS_PCT_Y_train.iloc[:, 0].mean()
                TS_PCT_naive_prediction = np.full(len(TS_PCT_Y_test), TS_PCT_naive_value)
                TS_PCT_naive_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_naive_prediction)
        
                USG_PCT_naive_value = USG_PCT_Y_train.iloc[:, 0].mean()
                USG_PCT_naive_prediction = np.full(len(USG_PCT_Y_test), USG_PCT_naive_value)
                USG_PCT_naive_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_naive_prediction)
                
                MPG_ratio = (MPG_Y_train.iloc[:, 0].mean()/ MPG_X_train.iloc[:, 0].mean())
                MPG_ratio_prediction = (MPG_X_test.iloc[:, 0] * MPG_ratio)
                MPG_ratio_mae = mean_absolute_error(MPG_Y_test, MPG_ratio_prediction)
    
                PPG_ratio = (PPG_Y_train.iloc[:, 0].mean()/ PPG_X_train.iloc[:, 0].mean())
                PPG_ratio_prediction = (PPG_X_test.iloc[:, 0] * PPG_ratio)
                PPG_ratio_mae = mean_absolute_error(PPG_Y_test, PPG_ratio_prediction)
                
                RPG_ratio = (RPG_Y_train.iloc[:, 0].mean()/ RPG_X_train.iloc[:, 0].mean())
                RPG_ratio_prediction = (RPG_X_test.iloc[:, 0] * RPG_ratio)
                RPG_ratio_mae = mean_absolute_error(RPG_Y_test, RPG_ratio_prediction)
                
                APG_ratio = (APG_Y_train.iloc[:, 0].mean()/ APG_X_train.iloc[:, 0].mean())
                APG_ratio_prediction = (APG_X_test.iloc[:, 0] * APG_ratio)
                APG_ratio_mae = mean_absolute_error(APG_Y_test, APG_ratio_prediction)
                
                TS_PCT_ratio = (TS_PCT_Y_train.iloc[:, 0].mean()/ TS_PCT_X_train.iloc[:, 0].mean())
                TS_PCT_ratio_prediction = (TS_PCT_X_test.iloc[:, 0] * TS_PCT_ratio)
                TS_PCT_ratio_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_ratio_prediction)
                
                USG_PCT_ratio = (USG_PCT_Y_train.iloc[:, 0].mean()/ USG_PCT_X_train.iloc[:, 0].mean())
                USG_PCT_ratio_prediction = (USG_PCT_X_test.iloc[:, 0] * USG_PCT_ratio)
                USG_PCT_ratio_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_ratio_prediction)
                
                
                print("MPG REGRESSION MAE:", round(MPG_mae, 3))
                print("PPG REGRESSION MAE:", round(PPG_mae, 3))
                print("RPG REGRESSION MAE:", round(RPG_mae, 3))
                print("APG REGRESSION MAE:", round(APG_mae, 3))
                print("TS_PCT REGRESSION MAE:", round(TS_PCT_mae, 3))
                print("USG_PCT REGRESSION MAE:", round(USG_PCT_mae, 3))
                print()
                print("MPG NAIVE MAE:", round(MPG_naive_mae, 3))
                print("PPG NAIVE MAE:", round(PPG_naive_mae, 3))
                print("RPG NAIVE MAE:", round(RPG_naive_mae, 3))
                print("APG NAIVE MAE:", round(APG_naive_mae, 3))
                print("TS_PCT NAIVE MAE:", round(TS_PCT_naive_mae, 3))
                print("USG_PCT NAIVE MAE:", round(USG_PCT_naive_mae, 3))
                print()
                print("MPG RATIO MAE:", round(MPG_ratio_mae, 3))
                print("PPG RATIO MAE:", round(PPG_ratio_mae, 3))
                print("RPG RATIO MAE:", round(RPG_ratio_mae, 3))
                print("APG RATIO MAE:", round(APG_ratio_mae, 3))
                print("TS_PCT RATIO MAE:", round(TS_PCT_ratio_mae, 3))
                print("USG_PCT RATIO MAE:", round(USG_PCT_ratio_mae, 3))
                
    def _2022_stats(self):
                matched = pd.read_csv(self.ncaa_translation_path) 
                
                season_data = matched["DRAFT_YEAR"]
                
                train_mask = season_data.isin([2018, 2019])
                test_mask = season_data == 2020
        
                MPG_X_data = matched[self.MPG_X]
                MPG_Y_data = matched[self.MPG_Y]
                MPG_X_train = MPG_X_data[train_mask]
                MPG_Y_train = MPG_Y_data[train_mask]
                MPG_X_test = MPG_X_data[test_mask]
                MPG_Y_test = MPG_Y_data[test_mask]
                MPG_model = LinearRegression() 
                MPG_model.fit(MPG_X_train, MPG_Y_train)
                
                PPG_X_data = matched[self.PPG_X]
                PPG_Y_data = matched[self.PPG_Y]
        
                
                PPG_X_train = PPG_X_data[train_mask]
                PPG_Y_train = PPG_Y_data[train_mask]
                PPG_X_test = PPG_X_data[test_mask]
                PPG_Y_test = PPG_Y_data[test_mask]
                PPG_model = LinearRegression() 
                PPG_model.fit(PPG_X_train, PPG_Y_train)
                
                RPG_X_data = matched[self.RPG_X]
                RPG_Y_data = matched[self.RPG_Y]
        
                RPG_X_train = RPG_X_data[train_mask]
                RPG_Y_train = RPG_Y_data[train_mask]
                RPG_X_test = RPG_X_data[test_mask]
                RPG_Y_test = RPG_Y_data[test_mask]
                RPG_model = LinearRegression() 
                RPG_model.fit(RPG_X_train, RPG_Y_train)
                
                APG_X_data = matched[self.APG_X]
                APG_Y_data = matched[self.APG_Y]
        
                
                APG_X_train = APG_X_data[train_mask]
                APG_Y_train = APG_Y_data[train_mask]
                APG_X_test = APG_X_data[test_mask]
                APG_Y_test = APG_Y_data[test_mask]
                APG_model = LinearRegression() 
                APG_model.fit(APG_X_train, APG_Y_train)
                
                TS_PCT_X_data = matched[self.TS_PCT_X]
                TS_PCT_Y_data = matched[self.TS_PCT_Y]
        
                
                TS_PCT_X_train = TS_PCT_X_data[train_mask]
                TS_PCT_Y_train = TS_PCT_Y_data[train_mask]
                TS_PCT_X_test = TS_PCT_X_data[test_mask]
                TS_PCT_Y_test = TS_PCT_Y_data[test_mask]
                TS_PCT_model = LinearRegression() 
                TS_PCT_model.fit(TS_PCT_X_train, TS_PCT_Y_train)
                
                USG_PCT_X_data = matched[self.USG_PCT_X]
                USG_PCT_Y_data = matched[self.USG_PCT_Y]
        
                
                USG_PCT_X_train = USG_PCT_X_data[train_mask]
                USG_PCT_Y_train = USG_PCT_Y_data[train_mask]
                USG_PCT_X_test = USG_PCT_X_data[test_mask]
                USG_PCT_Y_test = USG_PCT_Y_data[test_mask]
                USG_PCT_model = LinearRegression() 
                USG_PCT_model.fit(USG_PCT_X_train, USG_PCT_Y_train)
                
                test_info = matched.loc[test_mask, ["PLAYER_ID", "PLAYER_NAME", "DRAFT_YEAR"]].copy()
                
                MPG_prediction = MPG_model.predict(MPG_X_test).ravel()
                PPG_prediction = PPG_model.predict(PPG_X_test).ravel()
                RPG_prediction = RPG_model.predict(RPG_X_test).ravel()
                APG_prediction = APG_model.predict(APG_X_test).ravel()
                TS_PCT_prediction = TS_PCT_model.predict(TS_PCT_X_test).ravel()
                USG_PCT_prediction = USG_PCT_model.predict(USG_PCT_X_test).ravel()
                
                MPG_mae = mean_absolute_error(MPG_Y_test, MPG_prediction)
                PPG_mae = mean_absolute_error(PPG_Y_test, PPG_prediction)
                RPG_mae = mean_absolute_error(RPG_Y_test, RPG_prediction)
                APG_mae = mean_absolute_error(APG_Y_test, APG_prediction)
                TS_PCT_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_prediction)
                USG_PCT_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_prediction)
                
                MPG_result = pd.DataFrame()
                         
                MPG_result["ACTUAL_NBA_STAT"] = MPG_Y_test
                MPG_result["PREDICTED_NBA_STAT"] = MPG_prediction
                MPG_result["MAE"] = MPG_mae
                
                PPG_result = pd.DataFrame()
                         
                PPG_result["ACTUAL_NBA_STAT"] = PPG_Y_test
                PPG_result["PREDICTED_NBA_STAT"] = PPG_prediction
                PPG_result["MAE"] = PPG_mae
                
                RPG_result = pd.DataFrame()
                         
                RPG_result["ACTUAL_NBA_STAT"] = RPG_Y_test
                RPG_result["PREDICTED_NBA_STAT"] = RPG_prediction
                RPG_result["MAE"] = RPG_mae
                
                APG_result = pd.DataFrame()
                         
                APG_result["ACTUAL_NBA_STAT"] = APG_Y_test
                APG_result["PREDICTED_NBA_STAT"] = APG_prediction
                APG_result["MAE"] = APG_mae
                
                TS_PCT_result = pd.DataFrame()
                
                TS_PCT_result["ACTUAL_NBA_STAT"] = TS_PCT_Y_test
                TS_PCT_result["PREDICTED_NBA_STAT"] = TS_PCT_prediction
                TS_PCT_result["MAE"] = TS_PCT_mae
                
                USG_PCT_result = pd.DataFrame()
                
                USG_PCT_result["ACTUAL_NBA_STAT"] = USG_PCT_Y_test
                USG_PCT_result["PREDICTED_NBA_STAT"] = USG_PCT_prediction
                USG_PCT_result["MAE"] = USG_PCT_mae
                
                MPG_naive_value = MPG_Y_train.iloc[:, 0].mean()
                MPG_naive_prediction = np.full(len(MPG_Y_test), MPG_naive_value)
                MPG_naive_mae = mean_absolute_error(MPG_Y_test, MPG_naive_prediction)
        
        
                PPG_naive_value = PPG_Y_train.iloc[:, 0].mean()
                PPG_naive_prediction = np.full(len(PPG_Y_test), PPG_naive_value)
                PPG_naive_mae = mean_absolute_error(PPG_Y_test, PPG_naive_prediction)
        
        
                RPG_naive_value = RPG_Y_train.iloc[:, 0].mean()
                RPG_naive_prediction = np.full(len(RPG_Y_test), RPG_naive_value)
                RPG_naive_mae = mean_absolute_error(RPG_Y_test, RPG_naive_prediction)
        
        
                APG_naive_value = APG_Y_train.iloc[:, 0].mean()
                APG_naive_prediction = np.full(len(APG_Y_test), APG_naive_value)
                APG_naive_mae = mean_absolute_error(APG_Y_test, APG_naive_prediction)
        
        
                TS_PCT_naive_value = TS_PCT_Y_train.iloc[:, 0].mean()
                TS_PCT_naive_prediction = np.full(len(TS_PCT_Y_test), TS_PCT_naive_value)
                TS_PCT_naive_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_naive_prediction)
        
                USG_PCT_naive_value = USG_PCT_Y_train.iloc[:, 0].mean()
                USG_PCT_naive_prediction = np.full(len(USG_PCT_Y_test), USG_PCT_naive_value)
                USG_PCT_naive_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_naive_prediction)
                
                MPG_ratio = (MPG_Y_train.iloc[:, 0].mean()/ MPG_X_train.iloc[:, 0].mean())
                MPG_ratio_prediction = (MPG_X_test.iloc[:, 0] * MPG_ratio)
                MPG_ratio_mae = mean_absolute_error(MPG_Y_test, MPG_ratio_prediction)
    
                PPG_ratio = (PPG_Y_train.iloc[:, 0].mean()/ PPG_X_train.iloc[:, 0].mean())
                PPG_ratio_prediction = (PPG_X_test.iloc[:, 0] * PPG_ratio)
                PPG_ratio_mae = mean_absolute_error(PPG_Y_test, PPG_ratio_prediction)
                
                RPG_ratio = (RPG_Y_train.iloc[:, 0].mean()/ RPG_X_train.iloc[:, 0].mean())
                RPG_ratio_prediction = (RPG_X_test.iloc[:, 0] * RPG_ratio)
                RPG_ratio_mae = mean_absolute_error(RPG_Y_test, RPG_ratio_prediction)
                
                APG_ratio = (APG_Y_train.iloc[:, 0].mean()/ APG_X_train.iloc[:, 0].mean())
                APG_ratio_prediction = (APG_X_test.iloc[:, 0] * APG_ratio)
                APG_ratio_mae = mean_absolute_error(APG_Y_test, APG_ratio_prediction)
                
                TS_PCT_ratio = (TS_PCT_Y_train.iloc[:, 0].mean()/ TS_PCT_X_train.iloc[:, 0].mean())
                TS_PCT_ratio_prediction = (TS_PCT_X_test.iloc[:, 0] * TS_PCT_ratio)
                TS_PCT_ratio_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_ratio_prediction)
                
                USG_PCT_ratio = (USG_PCT_Y_train.iloc[:, 0].mean()/ USG_PCT_X_train.iloc[:, 0].mean())
                USG_PCT_ratio_prediction = (USG_PCT_X_test.iloc[:, 0] * USG_PCT_ratio)
                USG_PCT_ratio_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_ratio_prediction)
                
                
                print("MPG REGRESSION MAE:", round(MPG_mae, 3))
                print("PPG REGRESSION MAE:", round(PPG_mae, 3))
                print("RPG REGRESSION MAE:", round(RPG_mae, 3))
                print("APG REGRESSION MAE:", round(APG_mae, 3))
                print("TS_PCT REGRESSION MAE:", round(TS_PCT_mae, 3))
                print("USG_PCT REGRESSION MAE:", round(USG_PCT_mae, 3))
                print()
                print("MPG NAIVE MAE:", round(MPG_naive_mae, 3))
                print("PPG NAIVE MAE:", round(PPG_naive_mae, 3))
                print("RPG NAIVE MAE:", round(RPG_naive_mae, 3))
                print("APG NAIVE MAE:", round(APG_naive_mae, 3))
                print("TS_PCT NAIVE MAE:", round(TS_PCT_naive_mae, 3))
                print("USG_PCT NAIVE MAE:", round(USG_PCT_naive_mae, 3))
                print()
                print("MPG RATIO MAE:", round(MPG_ratio_mae, 3))
                print("PPG RATIO MAE:", round(PPG_ratio_mae, 3))
                print("RPG RATIO MAE:", round(RPG_ratio_mae, 3))
                print("APG RATIO MAE:", round(APG_ratio_mae, 3))
                print("TS_PCT RATIO MAE:", round(TS_PCT_ratio_mae, 3))
                print("USG_PCT RATIO MAE:", round(USG_PCT_ratio_mae, 3))
                
    def _2023_stats(self):
                matched = pd.read_csv(self.ncaa_translation_path) 
                
                season_data = matched["DRAFT_YEAR"]
                
                train_mask = season_data.isin([2018, 2019])
                test_mask = season_data == 2020
        
                MPG_X_data = matched[self.MPG_X]
                MPG_Y_data = matched[self.MPG_Y]
                MPG_X_train = MPG_X_data[train_mask]
                MPG_Y_train = MPG_Y_data[train_mask]
                MPG_X_test = MPG_X_data[test_mask]
                MPG_Y_test = MPG_Y_data[test_mask]
                MPG_model = LinearRegression() 
                MPG_model.fit(MPG_X_train, MPG_Y_train)
                
                PPG_X_data = matched[self.PPG_X]
                PPG_Y_data = matched[self.PPG_Y]
        
                
                PPG_X_train = PPG_X_data[train_mask]
                PPG_Y_train = PPG_Y_data[train_mask]
                PPG_X_test = PPG_X_data[test_mask]
                PPG_Y_test = PPG_Y_data[test_mask]
                PPG_model = LinearRegression() 
                PPG_model.fit(PPG_X_train, PPG_Y_train)
                
                RPG_X_data = matched[self.RPG_X]
                RPG_Y_data = matched[self.RPG_Y]
        
                RPG_X_train = RPG_X_data[train_mask]
                RPG_Y_train = RPG_Y_data[train_mask]
                RPG_X_test = RPG_X_data[test_mask]
                RPG_Y_test = RPG_Y_data[test_mask]
                RPG_model = LinearRegression() 
                RPG_model.fit(RPG_X_train, RPG_Y_train)
                
                APG_X_data = matched[self.APG_X]
                APG_Y_data = matched[self.APG_Y]
        
                
                APG_X_train = APG_X_data[train_mask]
                APG_Y_train = APG_Y_data[train_mask]
                APG_X_test = APG_X_data[test_mask]
                APG_Y_test = APG_Y_data[test_mask]
                APG_model = LinearRegression() 
                APG_model.fit(APG_X_train, APG_Y_train)
                
                TS_PCT_X_data = matched[self.TS_PCT_X]
                TS_PCT_Y_data = matched[self.TS_PCT_Y]
        
                
                TS_PCT_X_train = TS_PCT_X_data[train_mask]
                TS_PCT_Y_train = TS_PCT_Y_data[train_mask]
                TS_PCT_X_test = TS_PCT_X_data[test_mask]
                TS_PCT_Y_test = TS_PCT_Y_data[test_mask]
                TS_PCT_model = LinearRegression() 
                TS_PCT_model.fit(TS_PCT_X_train, TS_PCT_Y_train)
                
                USG_PCT_X_data = matched[self.USG_PCT_X]
                USG_PCT_Y_data = matched[self.USG_PCT_Y]
        
                
                USG_PCT_X_train = USG_PCT_X_data[train_mask]
                USG_PCT_Y_train = USG_PCT_Y_data[train_mask]
                USG_PCT_X_test = USG_PCT_X_data[test_mask]
                USG_PCT_Y_test = USG_PCT_Y_data[test_mask]
                USG_PCT_model = LinearRegression() 
                USG_PCT_model.fit(USG_PCT_X_train, USG_PCT_Y_train)
                
                test_info = matched.loc[test_mask, ["PLAYER_ID", "PLAYER_NAME", "DRAFT_YEAR"]].copy()
                
                MPG_prediction = MPG_model.predict(MPG_X_test).ravel()
                PPG_prediction = PPG_model.predict(PPG_X_test).ravel()
                RPG_prediction = RPG_model.predict(RPG_X_test).ravel()
                APG_prediction = APG_model.predict(APG_X_test).ravel()
                TS_PCT_prediction = TS_PCT_model.predict(TS_PCT_X_test).ravel()
                USG_PCT_prediction = USG_PCT_model.predict(USG_PCT_X_test).ravel()
                
                MPG_mae = mean_absolute_error(MPG_Y_test, MPG_prediction)
                PPG_mae = mean_absolute_error(PPG_Y_test, PPG_prediction)
                RPG_mae = mean_absolute_error(RPG_Y_test, RPG_prediction)
                APG_mae = mean_absolute_error(APG_Y_test, APG_prediction)
                TS_PCT_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_prediction)
                USG_PCT_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_prediction)
                
                MPG_result = pd.DataFrame()
                         
                MPG_result["ACTUAL_NBA_STAT"] = MPG_Y_test
                MPG_result["PREDICTED_NBA_STAT"] = MPG_prediction
                MPG_result["MAE"] = MPG_mae
                
                PPG_result = pd.DataFrame()
                         
                PPG_result["ACTUAL_NBA_STAT"] = PPG_Y_test
                PPG_result["PREDICTED_NBA_STAT"] = PPG_prediction
                PPG_result["MAE"] = PPG_mae
                
                RPG_result = pd.DataFrame()
                         
                RPG_result["ACTUAL_NBA_STAT"] = RPG_Y_test
                RPG_result["PREDICTED_NBA_STAT"] = RPG_prediction
                RPG_result["MAE"] = RPG_mae
                
                APG_result = pd.DataFrame()
                         
                APG_result["ACTUAL_NBA_STAT"] = APG_Y_test
                APG_result["PREDICTED_NBA_STAT"] = APG_prediction
                APG_result["MAE"] = APG_mae
                
                TS_PCT_result = pd.DataFrame()
                
                TS_PCT_result["ACTUAL_NBA_STAT"] = TS_PCT_Y_test
                TS_PCT_result["PREDICTED_NBA_STAT"] = TS_PCT_prediction
                TS_PCT_result["MAE"] = TS_PCT_mae
                
                USG_PCT_result = pd.DataFrame()
                
                USG_PCT_result["ACTUAL_NBA_STAT"] = USG_PCT_Y_test
                USG_PCT_result["PREDICTED_NBA_STAT"] = USG_PCT_prediction
                USG_PCT_result["MAE"] = USG_PCT_mae
                
                MPG_naive_value = MPG_Y_train.iloc[:, 0].mean()
                MPG_naive_prediction = np.full(len(MPG_Y_test), MPG_naive_value)
                MPG_naive_mae = mean_absolute_error(MPG_Y_test, MPG_naive_prediction)
        
        
                PPG_naive_value = PPG_Y_train.iloc[:, 0].mean()
                PPG_naive_prediction = np.full(len(PPG_Y_test), PPG_naive_value)
                PPG_naive_mae = mean_absolute_error(PPG_Y_test, PPG_naive_prediction)
        
        
                RPG_naive_value = RPG_Y_train.iloc[:, 0].mean()
                RPG_naive_prediction = np.full(len(RPG_Y_test), RPG_naive_value)
                RPG_naive_mae = mean_absolute_error(RPG_Y_test, RPG_naive_prediction)
        
        
                APG_naive_value = APG_Y_train.iloc[:, 0].mean()
                APG_naive_prediction = np.full(len(APG_Y_test), APG_naive_value)
                APG_naive_mae = mean_absolute_error(APG_Y_test, APG_naive_prediction)
        
        
                TS_PCT_naive_value = TS_PCT_Y_train.iloc[:, 0].mean()
                TS_PCT_naive_prediction = np.full(len(TS_PCT_Y_test), TS_PCT_naive_value)
                TS_PCT_naive_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_naive_prediction)
        
                USG_PCT_naive_value = USG_PCT_Y_train.iloc[:, 0].mean()
                USG_PCT_naive_prediction = np.full(len(USG_PCT_Y_test), USG_PCT_naive_value)
                USG_PCT_naive_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_naive_prediction)
                
                MPG_ratio = (MPG_Y_train.iloc[:, 0].mean()/ MPG_X_train.iloc[:, 0].mean())
                MPG_ratio_prediction = (MPG_X_test.iloc[:, 0] * MPG_ratio)
                MPG_ratio_mae = mean_absolute_error(MPG_Y_test, MPG_ratio_prediction)
    
                PPG_ratio = (PPG_Y_train.iloc[:, 0].mean()/ PPG_X_train.iloc[:, 0].mean())
                PPG_ratio_prediction = (PPG_X_test.iloc[:, 0] * PPG_ratio)
                PPG_ratio_mae = mean_absolute_error(PPG_Y_test, PPG_ratio_prediction)
                
                RPG_ratio = (RPG_Y_train.iloc[:, 0].mean()/ RPG_X_train.iloc[:, 0].mean())
                RPG_ratio_prediction = (RPG_X_test.iloc[:, 0] * RPG_ratio)
                RPG_ratio_mae = mean_absolute_error(RPG_Y_test, RPG_ratio_prediction)
                
                APG_ratio = (APG_Y_train.iloc[:, 0].mean()/ APG_X_train.iloc[:, 0].mean())
                APG_ratio_prediction = (APG_X_test.iloc[:, 0] * APG_ratio)
                APG_ratio_mae = mean_absolute_error(APG_Y_test, APG_ratio_prediction)
                
                TS_PCT_ratio = (TS_PCT_Y_train.iloc[:, 0].mean()/ TS_PCT_X_train.iloc[:, 0].mean())
                TS_PCT_ratio_prediction = (TS_PCT_X_test.iloc[:, 0] * TS_PCT_ratio)
                TS_PCT_ratio_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_ratio_prediction)
                
                USG_PCT_ratio = (USG_PCT_Y_train.iloc[:, 0].mean()/ USG_PCT_X_train.iloc[:, 0].mean())
                USG_PCT_ratio_prediction = (USG_PCT_X_test.iloc[:, 0] * USG_PCT_ratio)
                USG_PCT_ratio_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_ratio_prediction)
                
                
                print("MPG REGRESSION MAE:", round(MPG_mae, 3))
                print("PPG REGRESSION MAE:", round(PPG_mae, 3))
                print("RPG REGRESSION MAE:", round(RPG_mae, 3))
                print("APG REGRESSION MAE:", round(APG_mae, 3))
                print("TS_PCT REGRESSION MAE:", round(TS_PCT_mae, 3))
                print("USG_PCT REGRESSION MAE:", round(USG_PCT_mae, 3))
                print()
                print("MPG NAIVE MAE:", round(MPG_naive_mae, 3))
                print("PPG NAIVE MAE:", round(PPG_naive_mae, 3))
                print("RPG NAIVE MAE:", round(RPG_naive_mae, 3))
                print("APG NAIVE MAE:", round(APG_naive_mae, 3))
                print("TS_PCT NAIVE MAE:", round(TS_PCT_naive_mae, 3))
                print("USG_PCT NAIVE MAE:", round(USG_PCT_naive_mae, 3))
                print()
                print("MPG RATIO MAE:", round(MPG_ratio_mae, 3))
                print("PPG RATIO MAE:", round(PPG_ratio_mae, 3))
                print("RPG RATIO MAE:", round(RPG_ratio_mae, 3))
                print("APG RATIO MAE:", round(APG_ratio_mae, 3))
                print("TS_PCT RATIO MAE:", round(TS_PCT_ratio_mae, 3))
                print("USG_PCT RATIO MAE:", round(USG_PCT_ratio_mae, 3))
                
    def _2024_stats(self):
                matched = pd.read_csv(self.ncaa_translation_path) 
                
                season_data = matched["DRAFT_YEAR"]
                
                train_mask = season_data.isin([2018, 2019])
                test_mask = season_data == 2020
        
                MPG_X_data = matched[self.MPG_X]
                MPG_Y_data = matched[self.MPG_Y]
                MPG_X_train = MPG_X_data[train_mask]
                MPG_Y_train = MPG_Y_data[train_mask]
                MPG_X_test = MPG_X_data[test_mask]
                MPG_Y_test = MPG_Y_data[test_mask]
                MPG_model = LinearRegression() 
                MPG_model.fit(MPG_X_train, MPG_Y_train)
                
                PPG_X_data = matched[self.PPG_X]
                PPG_Y_data = matched[self.PPG_Y]
        
                
                PPG_X_train = PPG_X_data[train_mask]
                PPG_Y_train = PPG_Y_data[train_mask]
                PPG_X_test = PPG_X_data[test_mask]
                PPG_Y_test = PPG_Y_data[test_mask]
                PPG_model = LinearRegression() 
                PPG_model.fit(PPG_X_train, PPG_Y_train)
                
                RPG_X_data = matched[self.RPG_X]
                RPG_Y_data = matched[self.RPG_Y]
        
                RPG_X_train = RPG_X_data[train_mask]
                RPG_Y_train = RPG_Y_data[train_mask]
                RPG_X_test = RPG_X_data[test_mask]
                RPG_Y_test = RPG_Y_data[test_mask]
                RPG_model = LinearRegression() 
                RPG_model.fit(RPG_X_train, RPG_Y_train)
                
                APG_X_data = matched[self.APG_X]
                APG_Y_data = matched[self.APG_Y]
        
                
                APG_X_train = APG_X_data[train_mask]
                APG_Y_train = APG_Y_data[train_mask]
                APG_X_test = APG_X_data[test_mask]
                APG_Y_test = APG_Y_data[test_mask]
                APG_model = LinearRegression() 
                APG_model.fit(APG_X_train, APG_Y_train)
                
                TS_PCT_X_data = matched[self.TS_PCT_X]
                TS_PCT_Y_data = matched[self.TS_PCT_Y]
        
                
                TS_PCT_X_train = TS_PCT_X_data[train_mask]
                TS_PCT_Y_train = TS_PCT_Y_data[train_mask]
                TS_PCT_X_test = TS_PCT_X_data[test_mask]
                TS_PCT_Y_test = TS_PCT_Y_data[test_mask]
                TS_PCT_model = LinearRegression() 
                TS_PCT_model.fit(TS_PCT_X_train, TS_PCT_Y_train)
                
                USG_PCT_X_data = matched[self.USG_PCT_X]
                USG_PCT_Y_data = matched[self.USG_PCT_Y]
        
                
                USG_PCT_X_train = USG_PCT_X_data[train_mask]
                USG_PCT_Y_train = USG_PCT_Y_data[train_mask]
                USG_PCT_X_test = USG_PCT_X_data[test_mask]
                USG_PCT_Y_test = USG_PCT_Y_data[test_mask]
                USG_PCT_model = LinearRegression() 
                USG_PCT_model.fit(USG_PCT_X_train, USG_PCT_Y_train)
                
                test_info = matched.loc[test_mask, ["PLAYER_ID", "PLAYER_NAME", "DRAFT_YEAR"]].copy()
                
                MPG_prediction = MPG_model.predict(MPG_X_test).ravel()
                PPG_prediction = PPG_model.predict(PPG_X_test).ravel()
                RPG_prediction = RPG_model.predict(RPG_X_test).ravel()
                APG_prediction = APG_model.predict(APG_X_test).ravel()
                TS_PCT_prediction = TS_PCT_model.predict(TS_PCT_X_test).ravel()
                USG_PCT_prediction = USG_PCT_model.predict(USG_PCT_X_test).ravel()
                
                MPG_mae = mean_absolute_error(MPG_Y_test, MPG_prediction)
                PPG_mae = mean_absolute_error(PPG_Y_test, PPG_prediction)
                RPG_mae = mean_absolute_error(RPG_Y_test, RPG_prediction)
                APG_mae = mean_absolute_error(APG_Y_test, APG_prediction)
                TS_PCT_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_prediction)
                USG_PCT_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_prediction)
                
                MPG_result = pd.DataFrame()
                         
                MPG_result["ACTUAL_NBA_STAT"] = MPG_Y_test
                MPG_result["PREDICTED_NBA_STAT"] = MPG_prediction
                MPG_result["MAE"] = MPG_mae
                
                PPG_result = pd.DataFrame()
                         
                PPG_result["ACTUAL_NBA_STAT"] = PPG_Y_test
                PPG_result["PREDICTED_NBA_STAT"] = PPG_prediction
                PPG_result["MAE"] = PPG_mae
                
                RPG_result = pd.DataFrame()
                         
                RPG_result["ACTUAL_NBA_STAT"] = RPG_Y_test
                RPG_result["PREDICTED_NBA_STAT"] = RPG_prediction
                RPG_result["MAE"] = RPG_mae
                
                APG_result = pd.DataFrame()
                         
                APG_result["ACTUAL_NBA_STAT"] = APG_Y_test
                APG_result["PREDICTED_NBA_STAT"] = APG_prediction
                APG_result["MAE"] = APG_mae
                
                TS_PCT_result = pd.DataFrame()
                
                TS_PCT_result["ACTUAL_NBA_STAT"] = TS_PCT_Y_test
                TS_PCT_result["PREDICTED_NBA_STAT"] = TS_PCT_prediction
                TS_PCT_result["MAE"] = TS_PCT_mae
                
                USG_PCT_result = pd.DataFrame()
                
                USG_PCT_result["ACTUAL_NBA_STAT"] = USG_PCT_Y_test
                USG_PCT_result["PREDICTED_NBA_STAT"] = USG_PCT_prediction
                USG_PCT_result["MAE"] = USG_PCT_mae
                
                MPG_naive_value = MPG_Y_train.iloc[:, 0].mean()
                MPG_naive_prediction = np.full(len(MPG_Y_test), MPG_naive_value)
                MPG_naive_mae = mean_absolute_error(MPG_Y_test, MPG_naive_prediction)
        
        
                PPG_naive_value = PPG_Y_train.iloc[:, 0].mean()
                PPG_naive_prediction = np.full(len(PPG_Y_test), PPG_naive_value)
                PPG_naive_mae = mean_absolute_error(PPG_Y_test, PPG_naive_prediction)
        
        
                RPG_naive_value = RPG_Y_train.iloc[:, 0].mean()
                RPG_naive_prediction = np.full(len(RPG_Y_test), RPG_naive_value)
                RPG_naive_mae = mean_absolute_error(RPG_Y_test, RPG_naive_prediction)
        
        
                APG_naive_value = APG_Y_train.iloc[:, 0].mean()
                APG_naive_prediction = np.full(len(APG_Y_test), APG_naive_value)
                APG_naive_mae = mean_absolute_error(APG_Y_test, APG_naive_prediction)
        
        
                TS_PCT_naive_value = TS_PCT_Y_train.iloc[:, 0].mean()
                TS_PCT_naive_prediction = np.full(len(TS_PCT_Y_test), TS_PCT_naive_value)
                TS_PCT_naive_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_naive_prediction)
        
                USG_PCT_naive_value = USG_PCT_Y_train.iloc[:, 0].mean()
                USG_PCT_naive_prediction = np.full(len(USG_PCT_Y_test), USG_PCT_naive_value)
                USG_PCT_naive_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_naive_prediction)
                
                MPG_ratio = (MPG_Y_train.iloc[:, 0].mean()/ MPG_X_train.iloc[:, 0].mean())
                MPG_ratio_prediction = (MPG_X_test.iloc[:, 0] * MPG_ratio)
                MPG_ratio_mae = mean_absolute_error(MPG_Y_test, MPG_ratio_prediction)
    
                PPG_ratio = (PPG_Y_train.iloc[:, 0].mean()/ PPG_X_train.iloc[:, 0].mean())
                PPG_ratio_prediction = (PPG_X_test.iloc[:, 0] * PPG_ratio)
                PPG_ratio_mae = mean_absolute_error(PPG_Y_test, PPG_ratio_prediction)
                
                RPG_ratio = (RPG_Y_train.iloc[:, 0].mean()/ RPG_X_train.iloc[:, 0].mean())
                RPG_ratio_prediction = (RPG_X_test.iloc[:, 0] * RPG_ratio)
                RPG_ratio_mae = mean_absolute_error(RPG_Y_test, RPG_ratio_prediction)
                
                APG_ratio = (APG_Y_train.iloc[:, 0].mean()/ APG_X_train.iloc[:, 0].mean())
                APG_ratio_prediction = (APG_X_test.iloc[:, 0] * APG_ratio)
                APG_ratio_mae = mean_absolute_error(APG_Y_test, APG_ratio_prediction)
                
                TS_PCT_ratio = (TS_PCT_Y_train.iloc[:, 0].mean()/ TS_PCT_X_train.iloc[:, 0].mean())
                TS_PCT_ratio_prediction = (TS_PCT_X_test.iloc[:, 0] * TS_PCT_ratio)
                TS_PCT_ratio_mae = mean_absolute_error(TS_PCT_Y_test, TS_PCT_ratio_prediction)
                
                USG_PCT_ratio = (USG_PCT_Y_train.iloc[:, 0].mean()/ USG_PCT_X_train.iloc[:, 0].mean())
                USG_PCT_ratio_prediction = (USG_PCT_X_test.iloc[:, 0] * USG_PCT_ratio)
                USG_PCT_ratio_mae = mean_absolute_error(USG_PCT_Y_test, USG_PCT_ratio_prediction)
                
                
                print("MPG REGRESSION MAE:", round(MPG_mae, 3))
                print("PPG REGRESSION MAE:", round(PPG_mae, 3))
                print("RPG REGRESSION MAE:", round(RPG_mae, 3))
                print("APG REGRESSION MAE:", round(APG_mae, 3))
                print("TS_PCT REGRESSION MAE:", round(TS_PCT_mae, 3))
                print("USG_PCT REGRESSION MAE:", round(USG_PCT_mae, 3))
                print()
                print("MPG NAIVE MAE:", round(MPG_naive_mae, 3))
                print("PPG NAIVE MAE:", round(PPG_naive_mae, 3))
                print("RPG NAIVE MAE:", round(RPG_naive_mae, 3))
                print("APG NAIVE MAE:", round(APG_naive_mae, 3))
                print("TS_PCT NAIVE MAE:", round(TS_PCT_naive_mae, 3))
                print("USG_PCT NAIVE MAE:", round(USG_PCT_naive_mae, 3))
                print()
                print("MPG RATIO MAE:", round(MPG_ratio_mae, 3))
                print("PPG RATIO MAE:", round(PPG_ratio_mae, 3))
                print("RPG RATIO MAE:", round(RPG_ratio_mae, 3))
                print("APG RATIO MAE:", round(APG_ratio_mae, 3))
                print("TS_PCT RATIO MAE:", round(TS_PCT_ratio_mae, 3))
                print("USG_PCT RATIO MAE:", round(USG_PCT_ratio_mae, 3))
            
translator = TranslatingStats()

translator._2018_stats()