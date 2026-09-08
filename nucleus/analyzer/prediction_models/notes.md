# Notes from Running PredictorV1:

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

    S3:
        PPG          → sum
        PLUS_MINUS   → sum
        GP           → sum or average, depending meaning
        MPG          → average or weighted average
        USG_PCT      → weighted average
        TS_PCT       → weighted average

    RE-RUNNING TAKE_ALL_SEASONS AFTER S8:
        RESULTS FOR: 2017-18

            MAE: 0.07078207044741519
            Median Error: 5.800129843132272
            Naive MAE: 0.09189999999999997
            Naive MAE Wins: 7.535799999999997
            Simple MAE: 0.11949999999999998
            Simple MAE Wins: 9.798999999999998

                        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
            0   Cleveland Cavaliers        2017-18       2018-19           0.232           0.472657         19.024         38.757877          19.733877
            1       Milwaukee Bucks        2017-18       2018-19           0.732           0.578005         60.024         47.396412          12.627588
            2    Los Angeles Lakers        2017-18       2018-19           0.451           0.573918         36.982         47.061292          10.079292
            3  New Orleans Pelicans        2017-18       2018-19           0.402           0.519881         32.964         42.630230           9.666230
            4    Washington Wizards        2017-18       2018-19           0.390           0.506664         31.980         41.546447           9.566447


        RESULTS FOR: 2018-19

        MAE: 0.08990471697543129
        Median Error: 6.989494078516577
        Naive MAE: 0.09883333333333333
        Naive MAE Wins: 8.104333333333333
        Simple MAE: 0.13353333333333334
        Simple MAE Wins: 10.949733333333334

                    TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
        0  Golden State Warriors        2018-19       2019-20           0.231           0.474595         18.942         38.916784          19.974784
        1        Toronto Raptors        2018-19       2019-20           0.736           0.558823         60.352         45.823447          14.528553
        2         Boston Celtics        2018-19       2019-20           0.667           0.493117         54.694         40.435584          14.258416
        3        Detroit Pistons        2018-19       2019-20           0.303           0.475797         24.846         39.015359          14.169359
        4     Los Angeles Lakers        2018-19       2019-20           0.732           0.560336         60.024         45.947587          14.076413


        RESULTS FOR: 2019-20

            MAE: 0.08956312601538764
            Median Error: 6.655518892651582
            Naive MAE: 0.13103333333333333
            Naive MAE Wins: 10.744733333333333
            Simple MAE: 0.1157
            Simple MAE Wins: 9.4874

                            TEAM_NAME FEATURE_SEASON TARGET_SEASON  ...  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
            0         Toronto Raptors        2019-20       2020-21  ...         30.750         51.673896          20.923896
            1         Houston Rockets        2019-20       2020-21  ...         19.352         34.717890          15.365890
            2  Minnesota Timberwolves        2019-20       2020-21  ...         26.158         41.180498          15.022498
            3         New York Knicks        2019-20       2020-21  ...         46.658         33.219226          13.438774
            4      Philadelphia 76ers        2019-20       2020-21  ...         55.842         43.046734          12.795266

            [5 rows x 8 columns]


        RESULTS FOR: 2020-21

            MAE: 0.08022191291599905
            Median Error: 6.206119731134258
            Naive MAE: 0.0995
            Naive MAE Wins: 8.159
            Simple MAE: 0.11866666666666666
            Simple MAE Wins: 9.730666666666666

                            TEAM_NAME FEATURE_SEASON TARGET_SEASON  ...  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
            0         New York Knicks        2020-21       2021-22  ...         36.982         51.632670          14.650670
            1         Detroit Pistons        2020-21       2021-22  ...         22.960         36.688255          13.728255
            2      Los Angeles Lakers        2020-21       2021-22  ...         32.964         46.351966          13.387966
            3  Portland Trail Blazers        2020-21       2021-22  ...         26.978         39.735418          12.757418
            4   Golden State Warriors        2020-21       2021-22  ...         52.972         41.212763          11.759237

            [5 rows x 8 columns]


        RESULTS FOR: 2021-22

            MAE: 0.08140710510971517
            Median Error: 6.667532969511717
            Naive MAE: 0.0983
            Naive MAE Wins: 8.060599999999999
            Simple MAE: 0.09109999999999999
            Simple MAE Wins: 7.470199999999999

                        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
            0  Oklahoma City Thunder        2021-22       2022-23           0.488           0.259947         40.016         21.315684          18.700316
            1      San Antonio Spurs        2021-22       2022-23           0.268           0.470861         21.976         38.610601          16.634601
            2       Dallas Mavericks        2021-22       2022-23           0.463           0.624681         37.966         51.223855          13.257855
            3         Denver Nuggets        2021-22       2022-23           0.646           0.488921         52.972         40.091519          12.880481
            4      Charlotte Hornets        2021-22       2022-23           0.329           0.479445         26.978         39.314451          12.336451


        RESULTS FOR: 2022-23

            MAE: 0.09435381863785951
            Median Error: 7.384570411906001
            Naive MAE: 0.10323333333333332
            Naive MAE Wins: 8.465133333333332
            Simple MAE: 0.13659999999999997
            Simple MAE Wins: 11.201199999999998
            
                        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
            0   Memphis Grizzlies        2022-23       2023-24           0.329           0.601881         26.978         49.354225          22.376225
            1  Washington Wizards        2022-23       2023-24           0.183           0.451684         15.006         37.038053          22.032053
            2     Detroit Pistons        2022-23       2023-24           0.171           0.382267         14.022         31.345909          17.323909
            3     Toronto Raptors        2022-23       2023-24           0.305           0.501171         25.010         41.096008          16.086008
            4           Utah Jazz        2022-23       2023-24           0.378           0.538012         30.996         44.117017          13.121017


        RESULTS FOR: 2023-24

            MAE: 0.09959021047328842
            Median Error: 5.3939525392056815
            Naive MAE: 0.11139999999999997
            Naive MAE Wins: 9.134799999999998
            Simple MAE: 0.1292
            Simple MAE Wins: 10.5944

                        TEAM_NAME FEATURE_SEASON TARGET_SEASON  ACTUAL_WIN_PCT  PREDICTED_WIN_PCT  ACTUAL_WIN_82  PREDICTED_WIN_82  ABSOLUTE_ERROR_82
            0   New Orleans Pelicans        2023-24       2024-25           0.256           0.623181         20.992         51.100871          30.108871
            1     Philadelphia 76ers        2023-24       2024-25           0.293           0.559865         24.026         45.908954          21.882954
            2              Utah Jazz        2023-24       2024-25           0.207           0.464361         16.974         38.077612          21.103612
            3  Oklahoma City Thunder        2023-24       2024-25           0.829           0.623725         67.978         51.145468          16.832532
            4      Memphis Grizzlies        2023-24       2024-25           0.585           0.380818         47.970         31.227059          16.742941

# Notes from Running PredictorV2:

    Analysis after T7:
        Model	                        Avg MAE	    Avg MAE in wins
        Baseline only	                0.08655	    7.10 wins
        Baseline + NET impact	        0.08372	    6.87 wins
        Baseline + NET + RETURNING	    0.08485	    6.96 wins
    
    AFTER CONTINUITY REFINEMENT:
        RETURNING_SCORING_LOAD has been added to feature list self.X

    THOUGHT EXPERIMENT: SEASONAL INJURIES
        In the model, the 2019-20 Golden State Warriors were predicted to have a record of 37 wins, but only ended up with 18, where the assumption the model made was that Stephen Curry did not suffer a season-ending injury and rather grouped his played stats with the rest of the team. 
        
        So, TARGET_OLD_CORE_AVAILABILITY measured how available the core players from a previous season were in the target season and seeing if the metric has any correlation with PREDICTED & ABSOLUTE_ERROR_82. 

        RESULT: 
            PREDICTED_ERROR_82:
                                       count mean      median
                AVAILABILITY_BUCKET                           
                LOW                     49   4.344427  5.732124
                MEDIUM                 118  -0.515468 -0.305365
                HIGH                    43  -0.529919  0.571478

            ABSOLUTE_ERROR_82:
                                     count  mean      median
                AVAILABILITY_BUCKET                           
                LOW                     49  7.664860  6.737614
                MEDIUM                 118  6.865068  6.369614
                HIGH                    43  5.766467  5.753845

        OVERARCHING ANALYSIS:
            Teams with a HIGH and MEDIUM availability bucket do not show a crazy difference in team error wins, but there is a significant change when it comes to teams with a LOW availbility bucket.

    MODEL SWITCH-UP:
        Tried the following Models:
            - Linear Regression (with standardization)
            - Ridge Regression (with standardization)
            - Elastic Net (Lasso Regression)
            - Random Forest Regressor
            - Gradient Boosting Regressor

        Result: 
            Ridge was the best, with alpha = 7.0 being the best outcome.  

# Notes from NeuralNetworks:

Architecture:       13 → 10 → 5 → 1
Activation:         ReLU
Training loss:      MSE
Evaluation metric:  MAE
Optimizer:          Adam
Learning rate:      0.001
Seed:               42
Validation check:   every 10 epochs
Patience:           250 checks
Best epoch:         11520
Validation MAE:     0.025617

13 → 10 → 5 → 1
ReLU
Adam
lr = 0.001
seed = 42
patience = 250
validation check every 10 epochs

Take_All_Seasons:
2020-21 results: 
MAE: 0.08052195127596402
Median Error: 5.89137557534713
2021-22 results: 
MAE: 0.07907930733393428
Median Error: 6.210784295245812
2022-23 results: 
MAE: 0.07592100433905499
Median Error: 5.485128764493641
2023-24 results: 
MAE: 0.08752697680876881
Median Error: 6.7164197763440185
2024-25 results: 
MAE: 0.09823036481704839
Median Error: 5.843690018854602

Ridge rolling MAE: 0.08426
NN V1 rolling MAE: 0.08209

NN improvement: ~2.6%
Season wins:
Ridge 4
NN    1

TRYING DIFFERENT SEEDS

Seed: 0
2020-21 results: 
0.08181256859302519
Stopped at: 5090
Best epoch: 2590
Best validation MAE: 0.08181256800889969
2021-22 results: 
0.07119988539616268
Stopped at: 4900
Best epoch: 2400
Best validation MAE: 0.07119987905025482
2022-23 results: 
0.07356907826264697
Stopped at: 3250
Best epoch: 750
Best validation MAE: 0.07356907427310944
2023-24 results: 
0.08759906373023986
Stopped at: 6340
Best epoch: 3840
Best validation MAE: 0.08759906142950058
2024-25 results: 
0.10407847572962442
Stopped at: 3990
Best epoch: 1490
Best validation MAE: 0.10407847911119461

Seed: 1
2020-21 results: 
0.0721259387731552
Stopped at: 5390
Best epoch: 2890
Best validation MAE: 0.07212593406438828
2021-22 results: 
0.08057410128116607
Stopped at: 3980
Best epoch: 1480
Best validation MAE: 0.08057410269975662
2022-23 results: 
0.08768372286955516
Stopped at: 2940
Best epoch: 440
Best validation MAE: 0.08768371492624283
2023-24 results: 
0.08886409254868824
Stopped at: 3130
Best epoch: 630
Best validation MAE: 0.08886408805847168
2024-25 results: 
0.10754608250459036
Stopped at: 6420
Best epoch: 3920
Best validation MAE: 0.10754608362913132

Seed: 2
2020-21 results: 
0.08343234664996464
Stopped at: 6620
Best epoch: 4120
Best validation MAE: 0.08343233913183212
2021-22 results: 
0.07952481214205426
Stopped at: 3400
Best epoch: 900
Best validation MAE: 0.07952480763196945
2022-23 results: 
0.08521865199406942
Stopped at: 3960
Best epoch: 1460
Best validation MAE: 0.0852186530828476
2023-24 results: 
0.08701128338177998
Stopped at: 4870
Best epoch: 2370
Best validation MAE: 0.08701129257678986
2024-25 results: 
0.09710776900450388
Stopped at: 7780
Best epoch: 5280
Best validation MAE: 0.09710776805877686

Seed: 3
2020-21 results: 
0.09271061159769695
Stopped at: 3360
Best epoch: 860
Best validation MAE: 0.09271060675382614
2021-22 results: 
0.0720280742208163
Stopped at: 5640
Best epoch: 3140
Best validation MAE: 0.07202806323766708
2022-23 results: 
0.07697072483698526
Stopped at: 2960
Best epoch: 460
Best validation MAE: 0.07697071880102158
2023-24 results: 
0.08365074966748552
Stopped at: 5700
Best epoch: 3200
Best validation MAE: 0.08365074545145035
2024-25 results: 
0.09454244488080343
Stopped at: 8940
Best epoch: 6440
Best validation MAE: 0.09454243630170822

Seed: 4
2020-21 results: 
0.07499305236339568
Stopped at: 3500
Best epoch: 1000
Best validation MAE: 0.07499305158853531
2021-22 results: 
0.08713147766987485
Stopped at: 3310
Best epoch: 810
Best validation MAE: 0.08713147044181824
2022-23 results: 
0.0781989204486211
Stopped at: 2760
Best epoch: 260
Best validation MAE: 0.07819890975952148
2023-24 results: 
0.06560887047449747
Stopped at: 3750
Best epoch: 1250
Best validation MAE: 0.06560887396335602
2024-25 results: 
0.10451859352588654
Stopped at: 2990
Best epoch: 490
Best validation MAE: 0.1045185998082161

Seed: 42
2020-21 results: 
0.08280379719734192
Stopped at: 3480
Best epoch: 980
Best validation MAE: 0.08280380070209503
2021-22 results: 
0.08019077212015788
Stopped at: 4710
Best epoch: 2210
Best validation MAE: 0.08019077032804489
2022-23 results: 
0.07870804886817931
Stopped at: 3000
Best epoch: 500
Best validation MAE: 0.07870803773403168
2023-24 results: 
0.06832268094221751
Stopped at: 5980
Best epoch: 3480
Best validation MAE: 0.06832268089056015
2024-25 results: 
0.10041986924012501
Stopped at: 3620
Best epoch: 1120
Best validation MAE: 0.10041987150907516

Thus, NNV1 and Ridge are close, the former is not greater than the latter yet. 

WITH WEIGHT DECAY AT 0.0001:
Seed: 0
2020-21 results: 
0.0832878345966339
Stopped at: 4250
Best epoch: 1750
Best validation MAE: 0.08328782767057419
2021-22 results: 
0.07104045995076497
Stopped at: 4760
Best epoch: 2260
Best validation MAE: 0.07104045897722244
2022-23 results: 
0.0712658813079198
Stopped at: 3290
Best epoch: 790
Best validation MAE: 0.07126586884260178
2023-24 results: 
0.09124767136573791
Stopped at: 4220
Best epoch: 1720
Best validation MAE: 0.09124767035245895
2024-25 results: 
0.10253304105599721
Stopped at: 4280
Best epoch: 1780
Best validation MAE: 0.10253303498029709

Seed: 1
2020-21 results: 
0.07756741876999534
Stopped at: 5190
Best epoch: 2690
Best validation MAE: 0.07756742835044861
2021-22 results: 
0.0798925813039144
Stopped at: 3850
Best epoch: 1350
Best validation MAE: 0.0798925831913948
2022-23 results: 
0.08526110400358837
Stopped at: 2990
Best epoch: 490
Best validation MAE: 0.08526111394166946
2023-24 results: 
0.0892092647075653
Stopped at: 3110
Best epoch: 610
Best validation MAE: 0.08920925110578537
2024-25 results: 
0.10180982178052264
Stopped at: 7480
Best epoch: 4980
Best validation MAE: 0.10180982202291489

Seed: 2
2020-21 results: 
0.08755422314008077
Stopped at: 4010
Best epoch: 1510
Best validation MAE: 0.08755423128604889
2021-22 results: 
0.07890278204282127
Stopped at: 3520
Best epoch: 1020
Best validation MAE: 0.07890278846025467
2022-23 results: 
0.08435347964763641
Stopped at: 4090
Best epoch: 1590
Best validation MAE: 0.08435346931219101
2023-24 results: 
0.08515563581784565
Stopped at: 5250
Best epoch: 2750
Best validation MAE: 0.08515563607215881
2024-25 results: 
0.0991693104426066
Stopped at: 5890
Best epoch: 3390
Best validation MAE: 0.0991692990064621

Seed: 3
2020-21 results: 
0.08948078452746071
Stopped at: 3350
Best epoch: 850
Best validation MAE: 0.08948078751564026
2021-22 results: 
0.08058370796839398
Stopped at: 3600
Best epoch: 1100
Best validation MAE: 0.08058371394872665
2022-23 results: 
0.07054644799232482
Stopped at: 5940
Best epoch: 3440
Best validation MAE: 0.070546455681324
2023-24 results: 
0.08557791453202564
Stopped at: 5260
Best epoch: 2760
Best validation MAE: 0.08557792007923126
2024-25 results: 
0.10107268160184225
Stopped at: 3960
Best epoch: 1460
Best validation MAE: 0.10107266902923584

Seed: 4
2020-21 results: 
0.07428195097446438
Stopped at: 3570
Best epoch: 1070
Best validation MAE: 0.07428194582462311
2021-22 results: 
0.08673099604845046
Stopped at: 3170
Best epoch: 670
Best validation MAE: 0.08673099428415298
2022-23 results: 
0.07776433404286703
Stopped at: 2760
Best epoch: 260
Best validation MAE: 0.07776433974504471
2023-24 results: 
0.06818564478158949
Stopped at: 5540
Best epoch: 3040
Best validation MAE: 0.06818564981222153
2024-25 results: 
0.1007406953136126
Stopped at: 5640
Best epoch: 3140
Best validation MAE: 0.1007406935095787

Seed: 42
2020-21 results: 
0.07994224495093026
Stopped at: 4160
Best epoch: 1660
Best validation MAE: 0.0799422487616539
2021-22 results: 
0.07846675744056703
Stopped at: 4620
Best epoch: 2120
Best validation MAE: 0.07846676558256149
2022-23 results: 
0.07872421975135802
Stopped at: 3000
Best epoch: 500
Best validation MAE: 0.0787242203950882
2023-24 results: 
0.07111930468877156
Stopped at: 6160
Best epoch: 3660
Best validation MAE: 0.07111930102109909
2024-25 results: 
0.10032831749916074
Stopped at: 3600
Best epoch: 1100
Best validation MAE: 0.10032831132411957

WEIGHT DECAY = 0.001