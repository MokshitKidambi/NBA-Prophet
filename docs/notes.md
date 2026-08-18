Notes from Running PredictorV1:

    R1 Baseline Linear Regression:
        Mean Absolute Error = 0.10748 win% ≈ 8.81 wins

    R2 Error Analysis:
        Median error ≈ 7.44 wins

    Major issue:
        Extreme season-to-season changes produce 20–27 win errors (need to account for that).

    Hypothesis:
        Roster turnover, player availability, development, injuries,
        and personnel changes are missing explanatory variables.

    R3 Adding and Removing Features:
        Adding W_PCT:
            Mean MAE got worse
            Median Error went down
            Decision: keep for now, but a bit redundant 

        Removing PACE:
            Mean MAE: slightly worse
            Median error: better
            Worst misses: mostly unchanged
            Decision: not clearly beneficial

        Removing OREB_PCT:
            Mean MAE: very slightly better
            Median error: clearly better
            Worst misses: largely unchanged
            Current decision: Drop it

        Replacing NET_RATING with OFF_RATING + DEF_RATING:
            Mean MAE: much worse
            Median error: much worse
            Verdict: reject experiment
            Keep NET_RATING
    
    R4 — Walk-Forward Validation
        Test folds:
        2017-18 through 2023-24

        Average Linear Regression MAE:
        0.09551 win% ≈ 7.83 wins

        Average naive baseline: 
        ≈ 8.60 wins

        Average .500 baseline:
        ≈ 9.89 wins

        Finding:
        Current team-stat model adds predictive value across time, but major season-to-season roster/performance shifts remain the dominant source of large errors.

    5-Best Team Features(for now):
        NET_RATING
        TM_TOV_PCT 
        DREB_PCT 
        AST_RATIO 
        PACE

    RESULTS FROM TAKE_ALL_SEASONS:

        RESULTS FOR: 2017-18

        MAE: 0.07927930035179948
        Median Error: 4.787378619999917
        Naive MAE: 0.09189999999999997
        Naive MAE Wins: 7.535799999999997
        Simple MAE: 0.11949999999999998
        Simple MAE Wins: 9.798999999999998
        
        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
        0   Cleveland Cavaliers        2017-18       2018-19           0.232           0.522309         19.024         42.829338          23.805338
        1       Milwaukee Bucks        2017-18       2018-19           0.732           0.497765         60.024         40.816765          19.207235
        2       New York Knicks        2017-18       2018-19           0.207           0.430979         16.974         35.340265          18.366265
        3      Sacramento Kings        2017-18       2018-19           0.476           0.340211         39.032         27.897315          11.134685
        4  New Orleans Pelicans        2017-18       2018-19           0.402           0.534309         32.964         43.813323          10.849323


        RESULTS FOR: 2018-19

        MAE: 0.09016222895241252
        Median Error: 6.163483661527049
        Naive MAE: 0.09883333333333333
        Naive MAE Wins: 8.104333333333333
        Simple MAE: 0.13353333333333334
        Simple MAE Wins: 10.949733333333334

        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ...  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
        0   Golden State Warriors        2018-19       2019-20  ...         18.942         52.841261          33.899261
        1      Los Angeles Lakers        2018-19       2019-20  ...         60.024         39.418562          20.605438
        2         Detroit Pistons        2018-19       2019-20  ...         24.846         40.031346          15.185346
        3  Minnesota Timberwolves        2018-19       2019-20  ...         24.354         38.620630          14.266630
        4             LA Clippers        2018-19       2019-20  ...         55.842         43.578341          12.263659

        [5 rows x 8 columns]


        RESULTS FOR: 2019-20

        MAE: 0.11562359222464633
        Median Error: 8.777014280761897
        Naive MAE: 0.13103333333333333
        Naive MAE Wins: 10.744733333333333
        Simple MAE: 0.1157
        Simple MAE Wins: 9.4874

        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
        0        Houston Rockets        2019-20       2020-21           0.236           0.571707         19.352         46.879972          27.527972
        1        Toronto Raptors        2019-20       2020-21           0.375           0.636136         30.750         52.163142          21.413142
        2  Oklahoma City Thunder        2019-20       2020-21           0.306           0.543535         25.092         44.569838          19.477838
        3  Golden State Warriors        2019-20       2020-21           0.542           0.322178         44.444         26.418610          18.025390
        4        New York Knicks        2019-20       2020-21           0.569           0.359414         46.658         29.471979          17.186021


        RESULTS FOR: 2020-21

        MAE: 0.09254626144678103
        Median Error: 7.389950698280597
        Naive MAE: 0.0995
        Naive MAE Wins: 8.159
        Simple MAE: 0.11866666666666666
        Simple MAE Wins: 9.730666666666666

        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ...  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
        0          Indiana Pacers        2020-21       2021-22  ...         25.010         41.731488          16.721488
        1     Cleveland Cavaliers        2020-21       2021-22  ...         44.034         27.406953          16.627047
        2  Portland Trail Blazers        2020-21       2021-22  ...         26.978         42.703904          15.725904
        3            Phoenix Suns        2020-21       2021-22  ...         63.960         50.260364          13.699636
        4  Minnesota Timberwolves        2020-21       2021-22  ...         46.002         32.591285          13.410715

        [5 rows x 8 columns]


        RESULTS FOR: 2021-22

        MAE: 0.08414757528484752
        Median Error: 6.4960148391489
        Naive MAE: 0.0983
        Naive MAE Wins: 8.060599999999999
        Simple MAE: 0.09109999999999999
        Simple MAE Wins: 7.470199999999999

        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
        0      San Antonio Spurs        2021-22       2022-23           0.268           0.507016         21.976         41.575294          19.599294
        1       Sacramento Kings        2021-22       2022-23           0.585           0.396833         47.970         32.540273          15.429727
        2      Charlotte Hornets        2021-22       2022-23           0.329           0.516487         26.978         42.351895          15.373895
        3              Utah Jazz        2021-22       2022-23           0.451           0.619534         36.982         50.801814          13.819814
        4  Oklahoma City Thunder        2021-22       2022-23           0.488           0.334677         40.016         27.443519          12.572481


        RESULTS FOR: 2022-23

        MAE: 0.10849989600870993
        Median Error: 9.565888011914394
        Naive MAE: 0.10323333333333332
        Naive MAE Wins: 8.465133333333332
        Simple MAE: 0.13659999999999997
        Simple MAE Wins: 11.201199999999998

        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
        0     Washington Wizards        2022-23       2023-24           0.183           0.479156         15.006         39.290779          24.284779
        1      Memphis Grizzlies        2022-23       2023-24           0.329           0.582181         26.978         47.738861          20.760861
        2        Toronto Raptors        2022-23       2023-24           0.305           0.516066         25.010         42.317405          17.307405
        3        Detroit Pistons        2022-23       2023-24           0.171           0.347422         14.022         28.488622          14.466622
        4  Oklahoma City Thunder        2022-23       2023-24           0.695           0.518596         56.990         42.524866          14.465134


        RESULTS FOR: 2023-24

        MAE: 0.09831813301048416
        Median Error: 4.710853347326331
        Naive MAE: 0.11139999999999997
        Naive MAE Wins: 9.134799999999998
        Simple MAE: 0.1292
        Simple MAE Wins: 10.5944

        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
        0  New Orleans Pelicans        2023-24       2024-25           0.256           0.590882         20.992         48.452360          27.460360
        1    Philadelphia 76ers        2023-24       2024-25           0.293           0.551627         24.026         45.233453          21.207453
        2   Cleveland Cavaliers        2023-24       2024-25           0.780           0.552482         63.960         45.303525          18.656475
        3     Memphis Grizzlies        2023-24       2024-25           0.585           0.368048         47.970         30.179914          17.790086
        4       Detroit Pistons        2023-24       2024-25           0.537           0.327406         44.034         26.847328          17.186672