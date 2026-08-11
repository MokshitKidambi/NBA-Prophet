# Module 1: Team Stats

# 1.1: Traditional Stats

    Stat: PPG (Points Per Game)
    Formula(s): (Total Season Points)/82    OR    (Sum of (Player PPG * Player GP))/(82)
    Significance: More PPG => greater offensive success in the game
    Pros: Shows the team can score
    Cons: Does not show anything about defense 
    Predictive Value: High
        Justification: The most basic indicator at the end of a game on who wins is the team with the 
            most points, so this stat is hugely beneficial. 

    Stat: Opponent PPG (Opponent Points Per Game)
    Formula(s): (Total Season Points)/82
    Significance: Indicates how good a team is at stopping opponents from scoring
    Pros: Highlights the home team's defense
    Cons: Cannot be the only factor considered for winning games. 
    Predictive Value: High
        Justification: Same as PPG

    Stat: RPG (Rebounds Per Game)
    Formula(s): (Total Season Rebounds)/82
    Significance: More rebounds => more possessions to score
    Pros: Can see which team controls the paint area more (crucial for directing the game's flow)
    Cons: Doesn't tell anything about if the team scores off of most of the rebounds or not. 
    Predictive Value: Medium
        Justification: It is definitely good to track, but some advanced stats are better tracked for this engine's purpose. 

    Stat: APG (Assists Per Game)
    Formula(s): (Total Season Assists)/82
    Significance: Helps determine how the team primarily scores the ball (isolation, team effort, etc)
    Pros: Highlights team's ball movement ability
    Cons: An assist only counts when the recipient teammate makes the basket within two dribbles. 
    Predictive Value: High
        Justification: The assist means the team scored off of the pass, which would add to the team score. 

    Stat: TOPG (Turnovers Per Game)
    Formula(s): (Total Season Turnovers)/82
    Significance: More turnovers result in more possessions for the opponent. 
    Pros: Shows whether the team is good at keeping possession or not
    Cons: Teams with the more turnovers can still end up winning the game, so this stat shouldn't 
        absolutely followed. 
    Predictive Value: High
        Justification: Even with the con, it is still important to track this stat. 

    Stat: SPG (Steals Per Game)
    Formula(s): (Total Season Steals)/82
    Significance: steals are what lead to fast break opportunities and
        more openings to score. 
    Pros: Highlights the strength of the team's perimeter defense
    Cons: Same as turnover, but the fact that more steals does not technically mean it leads to guaranteed wins
    Predictive Value: Medium
        Justification: Same as con

    Stat: BPG (Blocks Per Game)
    Formula(s): (Total Season Blocks)/82
    Significance: Blocks help stop possessions on the court which limits the scoring chances for the 
        opponent. 
    Pros: Tracking this stat helps highlight the team's defense
    Cons: It does not indicate complete team defense
    Predictive Value: Medium
        Justification: It is more useful for individual than team, but still okay to consider.

    Stat: FPG (Fouls Per Game)
    Formula(s): (Total Fouls)/82
    Significance: Fouls slow the game down and penalize the team, leading to an advantage for the
        opponent. 
    Pros: Fouls can lead to momentum stops, more points for opponent, etc. 
    Cons: N/A
    Predictive Value: Medium
        Justification: Fouls in general are important to track, but the caveat is the way the fouls are
            committed (bad refereeing, late-game fouling, etc)
    
    Definitely Need:
        - PPG
        - Opponent PPG
        - RPG
        - APG
        - TOPG

    Maybe Need:
        - BPG
        - SPG
        - FPG

    Take Out:
        - N/A
    
    
# 1.2: Shooting Efficiency
    
    Stat: FG% (Field Goal Percentage)
    Formula(s): (Total Season FGM)/(Total Season FGA)
    Significance: Shows how efficient a team is at scoring the ball
    Pros: Can track efficiency
    Cons: Just because a team is more efficient does not mean that they ended up scoring more points
        than the opponent
    Predictive Value: Medium-High
        Justification: It is not really the most useful stat for this machine

    Stat: 3P% (Three-Point Percentage)
    Formula(s): (Total Season 3PM)/(Total Season 3PA)
    Significance: Displays a team's consistency at making 3 pointers
    Pros: Same as FG%
    Cons: Same reasoning as FG%
    Predictive Value: Medium
        Justification: Even with the con, 3 pointers dictate the game a lot in the modern era, so it is
            still somewhat important to track. 

    Stat: FT% (Free-Throw Percentage)
    Formula(s): (Total Season FTM)/(Total Season FTA)
    Significance: A team that is better at taking free throws is more likely to solidify leads throughout and/or at the end of the game
    Pros: Indicates how good a team is at taking advantage of free-throws with the rate they make them 
    Cons: This stat does not account for the amount of free-throws taken by each team. 
    Predictive Value: Medium-High
        Justification: With the addition of FTA, it is important to know the rate at which teams make
            the free-throws. 

    Stat: eFG% (Effective Field Goal Percentage)
    Formula(s): (FGM + 0.5 * 3PM)/(FGA)
    Significance: With the added worth of a 3-pointer, a normal FG% does not help make accurate
        inferences on which team is better at scoring. 
    Pros:  better indicator of a team's ability to score the ball, as it has more accurate and relevant 
        calculations than FG%
    Cons: Does not account for free-throws
    Predictive Value: High
        Justification: It is a better FG% to track that would actually help the engine predict game outcomes. 

    Stat: TS% (True Shooting Percentage)
    Formula(s): (PTS)/(2(FGA + 0.44 * FTA))
    Significance: It is a more complex stat than eFG%, as this tracks FG% including free-throws, as those
        shots usually do not count as actual field goals. 
    Pros: Helps identify how good a team is at shooting, which is the most important part of today's 
        basketball. 
    Cons: Not really useful for the engine
    Predictive Value: Medium
        Justification: For predicting wins, TS% is not as helpful as eFG% as it would better be used to 
            evaluate player performance instead. 
    
    Definitely Need:
        - eFG%
        - TS%

    Maybe Need:
        - FG%
        - 3P%
        - FT%

    Take Out:
        - N/A


# 1.3: Posession-Based Stats

    Stat: Pace
    Definition: Total possesions per game (48 minutes)
    Formula(s): (240/(Total Team Minutes))(Possession (opponent + team)/2)
    Significance: A greater pace usually equals more possessions which converts to more scoring chances. 
    Pros: Crucial for understanding which team is favored on the offensive side of the ball
    Cons: Does not track defense
    Predictive Value: Low-Medium
        Justification: To determine which team will win games, a team's pace is the perfect stat for
            offense, which can also be manipulated along with a defensive stat that would bringforth a formula for winning, but it does not automatically translate that a team with more pace is the better team 
    
    Stat: ORtg (Offensive Rating)
    Formula(s): 100 x ((total season points)/(total season possessions))
    Significance: Since the stat is points/possessions, it is a big indicator of which team has the
        stronger offense, as a number near or below 100 would suggest a bad offense relative to other teams
    Pros: Like pace, ORtg is huge for this engine to be able to determine which team will win a game 
    Cons: Same con as pace
    Predictive Value: High
        Justification: Combined with pace, offensive rating can really be utilized by the engine to
            state which team will score more points

    Stat: DRtg (Defensive Rating)
    Formula(s): 100 x ((total season opponent points)/(total possessions))
    Significance: The opposite of offensive rating; this stat can show how teams are on defense, with lower ratings indicating a stronger defense
    Pros: Same as ORtg but for defense
    Cons: Does not track offense
    Predictive Value: High
        Justification: This stat is the best identifier of the level of defense teams show against their
            opponents.  
    
    Stat: Net Rating
    Formula(s): ORtg - DRtg
    Significance: Takes the difference of both offensive rating and defensive rating
    Pros: Can actually be utilized highly to say which team can win the game before addressing player 
        matchups.
    Cons: The stat is an average across a team's matchup against every other team, so it cannot be the 
        sole factor used to predict individual games (this is where dynamic statistics come into play)
    Predictive Value: High
        Justification: Aside from the con, the first version of the engine will heavily need to utilize net rating to determine which team would win the game against their opponents
    
    
    Definitely Need:
        - ORtg
        - Drtg
        - Net Rating
    Maybe Need:
        - Pace
    Take Out: N/A


# 1.4: Possession Control

    Stat: TOV% (Turnover Percentage)
    Formula(s): 100 * (TOV/(FGA + 0.44*FTA + TOV))
    Significance: Tells how many of a team's possessions results in turnovers
    Pros: Shows if a team is good at handling and keeping possession
    Cons: Does not account for how the turnovers occured
    Predictive Value: Medium-High
        Justification: A greater turnover percentage shows the carelessness of teams in taking care of
            the ball, but it cannot be used as one of the main factors for winning. 
    
    Stat: ORB% (Offensive Rebound Percentage)
    Formula(s): 100 * (Team ORB/Total Game ORB)   OR   100 - DRB%
    Significance: Shows what percent of total offensive rebounds in a game belong to a certain team
    Pros: Offensive rebounds result in extra scoring opportunities
    Cons: Does not show how often those extra opportunities translate into made baskets
    Predictive Value: Medium
        Justification: This stat actually helps show which teams tend to dominate the glass, but for the
            first version of the model, it is not the most useful in this moment unless the disparity in the rebounds between teams are huge.
    
    Stat: DRB% (Defensive Rebound Percentage)
    Formula(s): 100 * (Team DRB/Total Game DRB)   OR   100 - ORB%
    Significance: Same as ORB% but it highlights the percent of a team's defensive rebounds
    Pros: Defensive rebounds prevent second chance opportunities for opponents
    Cons: Does not indicate anything about scoring
    Predictive Value: Medium-High
        Justification: Same as ORB%
    
    Stat: AST Ratio (Assist Ratio)
    Formula(s): (Total Team AST * 100) / (Total Team POSS)   OR   (Total Team AST x 100)/(FGA + (FTA *
        0.44) + Total Team AST + Total Team TO)
    Significance: For a player, it is the proportion of assists they contribute out of the team total.
        For the team, it is the ratio that shows the number of possessions that result in assists.
    Pros: Highly indicative of the type of offense a team runs
    Cons: A small assist ratio does not indicate that the team does not score points; some buckets could
        be generated off of passes but might not count as a assist because of multiple dribbles before scoring. 
    Predictive Value: Medium
        Justification: Compared to APG, this stat is better suited for this engine because of the value
            it gives to assists instead of just representing it as a static number. But again, assists are not the biggest indicator of winning as they are just the TYPE of baskets scored by a team.
    
    Stat: AST% (Assist Percentage)
    Formula(s): 100 * (Player Total AST) / [{((Total Player MP)/((Total Teammate MP)/5)) * Total Teammate FGA} - FG]
    Significance: For a player, its their contribution to teammate scoring when they are both playing at
        the same time. 
    Pros: Indicates the playmaking capabilities of a player
    Cons: Does not really mean anything for the engine because team stats are more important than  
        individual, but can later be used for individual stats.
    Predictive Value: Medium
        Justification: It is easier to work with ratios than percentages so that is why its predictive
            value is lower than assist ratio.
    
    Definitely Need:
        - TOV%
    
    Maybe Need:
        - ORB%
        - DRB%
        - AST Ratio (Can replace APG)
    
    Individual Priority:
        - AST%
    
    Take Out: N/A
    
# Summary

- Would Keep
    -  PPG       
        - Scoring
        - Basic offensive production
    - Opp PPG
        - Defense
        - Basic defensive production
    - eFG%
        - Efficiency
        - Shooting efficiency
    - TS% 
        - Efficiency
        - Overall scoring efficiency
    - ORtg
        - Possessions
        - Offensive efficiency
    - DRtg
        - Possessions
        - Defensive efficiency
    - Net Rating
        - Possessions
        - Overall team strength

- Might Keep:
    - Pace
        - Possessions
        - Game tempo          
    - TOV%
        - Possession control
        - Possession preservation
    - ORB%
        - Possession control
        - Extra possessions   
    - DRB%
        - Possession control
        - Prevents second chances
    - AST Ratio
        - Possession control
        - Passing efficiency  

- Initial Features
    - PPG
        - Highlights the main part of scoring
    - Opponent PPG
        - Shows how effective the defense really is
    - TS%
        - Displays how well teams can score
    - Net Rating
        - How good teams are in general
    - TOV%
        - How good teams are at handling the ball
    - ORB%
        - How good teams are at creating extra chances through rebounds
    - DRB%
        - How consistently can teams close their opponent's possessions
    - AST Ratio
        - How well the ball is distributed and how often it leads to points
