# Module 2: Individual Player Stats

# 2.1: Basic Stats
    Stat: PPG (Points Per Game)
    Formula(s): (Total Season Points)/GP
    Significance: Shows the player's average scoring output
    Pros: Players who score more points tend to help towards winning
    Cons: It does not account for efficiency
    Predictive Value: Medium-High
        Justification: It is the main stat of a player that matters in terms of team contribution, but 
            there are other advanced metrics that would outweigh pure PPG. 
    
    Stat: RPG (Rebounds Per Game)
    Formula(s): (Total Season Rebounds)/GP
    Significance: More rebounds => more possessions to score
    Pros: Can see which player controls the paint area the most (crucial for directing the game's flow)
    Cons: Doesn't tell anything about if the player/team scores off of most of the rebounds or not. 
    Predictive Value: Medium
        Justification: It is definitely good to track, but some advanced stats are better tracked for   
            this engine's purpose. 
    
    Stat: APG (Assists Per Game)
    Formula(s): (Total Season Assists)/GP
    Significance: Helps determine the play-style of a player and how they sets up their team on offense
    Pros: Highlights team's ball movement ability
    Cons: An assist only counts when the recipient teammate makes the basket within two dribbles. 
    Predictive Value: Medium-High
        Justification: The assist means the team scored off of the pass, which would add to the team
            score. 
    
    Stat: SPG (Steals Per Game)
    Formula(s): (Total Season Steals)/GP
    Significance: Steals are what lead to fast break opportunities and more openings to score. 
    Pros: Highlights the strength of the player's perimeter defense
    Cons: Steals should not be the only metric that should be considered for a player's defensive
        contribution.
    Predictive Value: High
        Justification: Still important to have SPG
    
    Stat: BPG (Blocks Per Game)
    Formula(s): (Total Season Blocks)/GP
    Significance: Blocks help stop possessions on the court which limits the scoring chances for the 
        opponent. 
    Pros: Tracking this stat helps highlight the team's defense
    Cons: It does not indicate complete team defense
    Predictive Value: Medium
        Justification: It is more useful for individual than team, but still okay to consider.

    
    Stat: TOV (Turnovers)
    Formula(s): (Total Season Turnovers)/GP
    Significance: More turnovers result in more possessions for the opponent. 
    Pros: Shows whether the player is good at keeping possession or not
    Cons: Turnovers can be caused by many factors, so it does not automatically mean the player is not 
        good at handling the ball. 
    Predictive Value: High
        Justification: Even with the con, it is still important to track this stat.


# 2.2: Player Efficiency
    Stat: eFG% (Effective Field Goal Percentage)
    Formula(s): (FGM + 0.5 * 3PM)/(FGA)
    Significance: With the added worth of a 3-pointer, a normal FG% does not help make accurate
        inferences on how efficiently a player scores the ball. 
    Pros:  Better indicator of a player's efficiency, as it has more accurate and relevant 
        calculations than FG%
    Cons: Does not account for free-throws
    Predictive Value: Medium-High
        Justification: It is hugely beneficial to the team as player efficiency contributes to overall
            team efficiency.

    Stat: TS% (True Shooting Percentage)
    Formula(s): (PTS)/(2(FGA + 0.44 * FTA))
    Significance: It is a more complex stat than eFG%, as this tracks FG% including free-throws, as those
        shots usually do not count as actual field goals. 
    Pros: Helps identify the level of scoring efficiency, which is the most important part of today's 
        basketball. 
    Cons: Does not concern usage rate
    Predictive Value: Medium-High
        Justification: Contrasting eFG%, it is a more beneficial stat than eFG% since this also accounts
            for free-throws, which is also important to consider when looking at player contribution. 
    

# 2.3: Usage & Offensive Responsibility
    Stat: USG% (Usage Rate)
    Formula(s): (FGA + Possession Ending FTA + TOV) / POSS
    Significance: Some players have the ball more than others, so this needs to go along with efficiency
        to truly determine player contribution. 
    Pros: Shows how much a team relies on a player on the offensive side of the ball
    Cons: Just because they have the ball more does not automatically mean they are more efficient or 
        that they score better than a player who has a lower usage rate. 
    Predictive Value: Medium-High
        Justification: The stat is definitely important, but it can truly be utilized when combined with
            an efficiency tracking stat like eFG% or TS%. 
    
    
 # 2.4: Advanced Impact Metrics
    Stat: BPM (Box Plus/Minus)
    Formula(s): N/A
    Significance: Rating of a player compared to an average player in the league. 
    Pros: Good way of showing player contribution
    Cons: Heavily relies on box score stats 
    Predictive Value: Medium-High
        Justification: It is definitely a useful stat to measure contribution but it cannot be used as a
            primary resource to measure that value. 
    
    Stat: VORP (Value Over Replacement Player)
    Formula(s): (BPM - (-2.0)) * (% of possessions) * (games played/82)
    Significance: Really good way of measuring player contribution
    Pros: Factors in minutes played so it is not just covering who temporarily has the most impact
    Cons: Need to find BPM in order to derive this stat, which is a bit extra.
    Predictive Value: High
        Justification: Aside from the con, it still really important to have this stat. 
    
    Stat: Win Shares / WS/48
    Formula(s): Offensive Win Shares + Defensive Win Shares
        Offensive Win Shares: (marginal offense) / (marginal points per win)
        Defensive Win Shares: (marginal defense) / (marginal points per win)

        WS/48: Win Shares over 48 minutes
    Significance: Estimates how many wins each person added to the team through their individual
        effort
    Pros: Can directly see who contributes the most
    Cons: Should not be relied upon completely as it is based off of statistical calculations
    Predictive Value: High but Medium-High for WS/48
        Justification: con is negligible here because of the value produced by the pro. 
    
    Stat: PER (Player Efficiency Rating)
    Formula(s): Pretty long
    Significance: Measures how efficient a player is on the court. 
    Pros: Can use the ratings of each player to compare with one another
    Cons: Very relative to a player's respective era (not really useful when comparing past players) and
        bases the rating off of box score stats
    Predictive Value: Medium
        Justification: In addition to the con, it is formulated using hard stats such as ppg and assists,
            which can be deceiving. 


# 2.5: On & Off Impact
    Stat: Plus/Minus
    Formula(s): Difference of Scores accumulated in the time that a player is on the court.
    Significance: It shows how good the team is when a certain player is playing.
    Pros: Good way of showing player contribution
    Cons: A player with a low plus/minus does not necessarily mean that they are causing the low number,
    as it could be a total defensive breakdown or an offensive surge by the opponent that does not involve that player.
    Predictive Value: Medium-High
    Justification: It is definitely a useful stat to measure contribution but it cannot be used as a
        primary resource to measure that value.
    
    Stat: On/Off
    Formula(s): Plus/Minus when player is playing - Plus/Minus when player is on the bench
    Significance: Indicates if a team plays well with a certain player on the court or not
    Pros: Player with a positive on/off rating means they are somewhat valuable to the team.
    Cons: Similar to the con with plus/minus, the stat does depend on a lot of factors outside of an 
        individual player's control
    Predictive Value: Medium
        Justification: Same reasoning as plus/minus


# 2.6: Availability
    Stat: GP (Games Played)
    Formula(s): N/A
    Significance: Shows how many games a player played 
    Pros: Helps with determining a lot of other stats like VORP
    Cons: It alone cannot provide any conclusions
    Predictive Value: High
        Justification: Important for calculating other stats which will be useful to determine player
            contribution. 
    
    Stat: MPG
    Formula(s): (Total Minutes Played) / (GP)
    Significance: How many minutes a player averages in a game
    Pros: Shows how often each player plays and, like GP, is used in other important stats
    Cons: Same as GP
    Predictive Value: Medium
        Justification: Same as GP
    
    Stat: Multi-Season Availability
    Formula(s): N/A
    Significance: Player avilability is crucial in determining how games/matchups would play out
    Pros: Players who are more available than others are able to help their team more 
    Cons: Does not say anything about whether the player is good during their available time on the court
    Predictive Value: High
        Justification: In terms of a whole regular season, this is very important
    
    Stat: Games Missed
    Formula(s): 82 - GP
    Significance: When a player misses a lot of games, they fall out of rotation and not only is their 
        production missed on the court, but they are off-rhythm when they come back. 
    Pros: Shows who can be relied upon to be available
    Cons: Does not suggest anything about the player's level of play on the court
    Predictive Value: Low
        Justification: Not the most useful by itself, but its implications are pretty significant
    
    Stat: Injury History
    Formula(s): N/A
    Significance: A player with an injury history is more likely to be unavailable during the regular
        season.
    Pros: Shows who can be relied upon to be available
    Cons: Does not suggest anything about the player's level of play on the court
    Predictive Value: Medium-High
        Justification: Not the most useful by itself, but its implications are pretty significant
    
    
# Summary
    
- Initial Features
    - PPG
    - MPG
    - TS%
    - USG%
    - VORP
    - GP
    - Multi-Season Availability

- Might Keep
    - BPM
    - RPG
    - APG
    - SPG
    - BPG
    - TOV
    - eFG%
    - Win Shares
    - WS/48
    - PER
    - Plus/Minus
    - On/Off
    - Injury History

- Take Out
    - Games Missed


    
    
    
       
    
    