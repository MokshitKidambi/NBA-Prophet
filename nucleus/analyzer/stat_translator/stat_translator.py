import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

class StatTranslator:
    def __init__(self, path, draft_years):
        self.path = path
        self.draft_years = draft_years

        self.stats = [
            "MPG",
            "PPG",
            "RPG",
            "APG",
            "TS_PCT",
            "USG_PCT"
        ]
    
    def validate_year(self, test_year):
        matched = pd.read_csv(self.path)

        train_mask = matched["DRAFT_YEAR"].isin(
            [year for year in self.draft_years if year != test_year]
        )

        test_mask = matched["DRAFT_YEAR"] == test_year

        for stat in self.stats:
            X_col = f"PRE_NBA_{stat}"
            Y_col = f"FIRST_VALUABLE_NBA_{stat}"

            valid_mask = (
                matched[X_col].notna()
                & matched[Y_col].notna()
            )

            stat_train_mask = train_mask & valid_mask
            stat_test_mask = test_mask & valid_mask

            X_train = matched.loc[stat_train_mask, [X_col]]
            Y_train = matched.loc[stat_train_mask, Y_col]

            X_test = matched.loc[stat_test_mask, [X_col]]
            Y_test = matched.loc[stat_test_mask, Y_col]
            
            model = LinearRegression()
            model.fit(X_train, Y_train)

            reg_prediction = model.predict(X_test)

            naive_value = Y_train.mean()
            naive_prediction = np.full(len(Y_test), naive_value)

            ratio = Y_train.mean() / X_train.iloc[:, 0].mean()
            ratio_prediction = X_test.iloc[:, 0] * ratio
            
            reg_mae = mean_absolute_error(Y_test, reg_prediction)
            naive_mae = mean_absolute_error(Y_test, naive_prediction)
            ratio_mae = mean_absolute_error(Y_test, ratio_prediction)
            print(test_year, stat)
            print(f"Reg MAE: {reg_mae}")
            print(f"Naive MAE: {naive_mae}")
            print(f"Ratio MAE: {ratio_mae}")
            print()
    
    def validate_all_years(self):
        for year in self.draft_years:
            self.validate_year(year)
    
    def finale_regression(self):
            matched = pd.read_csv(self.path)
            
            final_MPG_value = matched["FIRST_VALUABLE_NBA_MPG"].mean()
            
            ppg_ratio = matched["FIRST_VALUABLE_NBA_PPG"].mean() / matched["PRE_NBA_PPG"].mean()
                        
            final_RPG_value = matched["FIRST_VALUABLE_NBA_RPG"].mean()
            
            apg_ratio = matched["FIRST_VALUABLE_NBA_APG"].mean() / matched["PRE_NBA_APG"].mean()

            final_TS_value = matched["FIRST_VALUABLE_NBA_TS_PCT"].mean()
            
            usg_ratio = matched["FIRST_VALUABLE_NBA_USG_PCT"].mean() / matched["PRE_NBA_USG_PCT"].mean()
                                    
            print("FINAL MPG VALUE:", round(final_MPG_value, 3))
                
            print("PPG Ratio: ", round(ppg_ratio, 4))
    
            print("FINAL RPG VALUE:", round(final_RPG_value, 3))
    
            print("APG Ratio: ", round(apg_ratio, 4))
    
            print("FINAL TS VALUE:", round(final_TS_value, 3))
    
            print("USG Ratio: ", round(usg_ratio, 4))

            self.final_MPG_value = final_MPG_value
            self.predicted_ppg_ratio = ppg_ratio
            self.final_RPG_value = final_RPG_value
            self.predicted_apg_ratio = apg_ratio
            self.final_TS_value = final_TS_value
            self.predicted_usg = usg_ratio 
            
    def assign_stats(self):
            rookies = pd.read_csv("rookies.csv")
            ncaa_mask = rookies["ROOKIE_SOURCE"] == "NCAA"
            
            rookies.loc[ncaa_mask, "TRANSLATED_MPG"] = 19.747
            rookies.loc[ncaa_mask, "TRANSLATED_PPG"] = (4.5159 + 0.2235 * rookies.loc[ncaa_mask, "PPG"])
            rookies.loc[ncaa_mask, "TRANSLATED_RPG"] = (1.0218 + 0.4116 * rookies.loc[ncaa_mask, "RPG"])
            rookies.loc[ncaa_mask, "TRANSLATED_APG"] = (0.4165 + 0.4974 * rookies.loc[ncaa_mask, "APG"])
            rookies.loc[ncaa_mask, "TRANSLATED_TS_PCT"] = (0.3990 + 0.2349 * rookies.loc[ncaa_mask, "TS_PCT"])
            rookies.loc[ncaa_mask, "TRANSLATED_USG_PCT"] = (0.0886 + 0.3355 * rookies.loc[ncaa_mask, "USG_PCT"])      
            
            cols = [
                "PLAYER_NAME",
                "PPG", "TRANSLATED_PPG",
                "RPG", "TRANSLATED_RPG",
                "APG", "TRANSLATED_APG",
                "TS_PCT", "TRANSLATED_TS_PCT",
                "USG_PCT", "TRANSLATED_USG_PCT",
            ]
    
            print(rookies.loc[ncaa_mask, cols].head(15))
            print(
                rookies.loc[
                    ncaa_mask,
                    [
                        "TRANSLATED_MPG",
                        "TRANSLATED_PPG",
                        "TRANSLATED_RPG",
                        "TRANSLATED_APG",
                        "TRANSLATED_TS_PCT",
                        "TRANSLATED_USG_PCT",
                    ]
                ].describe()
            )
            
            international_mask = rookies["ROOKIE_SOURCE"] == "INTERNATIONAL"
            
            rookies.loc[international_mask, "TRANSLATED_MPG"] = 21.424
            rookies.loc[international_mask, "TRANSLATED_PPG"] = rookies.loc[international_mask, "PPG"] * 0.8705
            rookies.loc[international_mask, "TRANSLATED_RPG"] = 1.2109 + 0.6939 * rookies.loc[international_mask, "RPG"]
            rookies.loc[international_mask, "TRANSLATED_APG"] = 0.5508 + 0.7772 * rookies.loc[international_mask, "APG"]
            rookies.loc[international_mask, "TRANSLATED_TS_PCT"] = 0.3687 + 0.2614 * rookies.loc[international_mask, "TS_PCT"]
            rookies.loc[international_mask, "TRANSLATED_USG_PCT"] = rookies.loc[international_mask, "USG_PCT"] * 0.8204 
    
            print(rookies.loc[international_mask, cols].head(15))
            print(
                rookies.loc[
                    international_mask,
                    [
                        "TRANSLATED_MPG",
                        "TRANSLATED_PPG",
                        "TRANSLATED_RPG",
                        "TRANSLATED_APG",
                        "TRANSLATED_TS_PCT",
                        "TRANSLATED_USG_PCT",
                    ]
                ].describe()
            )
            
            g_league_mask = rookies["ROOKIE_SOURCE"] == "G-LEAGUE"

            rookies.loc[g_league_mask, "TRANSLATED_MPG"] = 19.725

            rookies.loc[g_league_mask, "TRANSLATED_PPG"] = (
                rookies.loc[g_league_mask, "PPG"] * 0.5591
            )

            rookies.loc[g_league_mask, "TRANSLATED_RPG"] = 2.912

            rookies.loc[g_league_mask, "TRANSLATED_APG"] = (
                rookies.loc[g_league_mask, "APG"] * 0.5667
            )

            rookies.loc[g_league_mask, "TRANSLATED_TS_PCT"] = 0.544

            rookies.loc[g_league_mask, "TRANSLATED_USG_PCT"] = (
                rookies.loc[g_league_mask, "USG_PCT"] * 0.8478
            )
            
            print(rookies.loc[g_league_mask, cols].head(15))
            print(
                rookies.loc[
                    g_league_mask,
                    [
                        "TRANSLATED_MPG",
                        "TRANSLATED_PPG",
                        "TRANSLATED_RPG",
                        "TRANSLATED_APG",
                        "TRANSLATED_TS_PCT",
                        "TRANSLATED_USG_PCT",
                    ]
                ].describe()
            )
            
            rookies.to_csv("rookies_translated.csv", index = False)            
                        
class NCAATranslator(StatTranslator):
    def __init__(self):
        super().__init__(
            path="ncaa_translation_sample.csv",
            draft_years=list(range(2018, 2025))
        )

class InternationalTranslator(StatTranslator):
    def __init__(self):
        super().__init__(
            path="inter_translation.csv",
            draft_years=list(range(2017, 2025))
        )
        
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
        
class GLeagueTranslator(StatTranslator):
    def __init__(self):
        super().__init__(
            path="g_league_translation.csv",
            draft_years=[2021, 2022, 2023, 2024]
        )
        
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
        
ncaa = NCAATranslator()
international = InternationalTranslator()
g_league = GLeagueTranslator()

g_league.assign_stats()