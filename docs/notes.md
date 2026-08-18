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