# Preface
    Instead of going with a generic weather project for Gear 3, I decided to switch it up and do something related to the things 
        I like, which happens to be sports. 

    To be more specific, this project is about using NBA analytics about all 30 teams to predict their record in the upcoming 
        2026-2027 regular season. 

    I can fetch APIs that have statistics like team PPG, RPG, APG, defense, etc. To deal with new players being added to many 
        rosters [except the warriors :( ], I can factor in individual PPG of those newly added players and add them to the team PPG,
        while subtracting the PPG lost from players leaving that team in the off-season. 

    To account for injuries, I can take a look at the games played across recent years for the players on each team, and if they have 
        played 65 games or more, then that player can be considered healthy and their contributions for their team can be considered
        meaningful and can be taken into account. 

        If the player averaged between 40 to 65 games played, then the player would be considered somewhat healthy, and their teams' 
        statistics would be somewhat affected. 

        However, if the player averages less than 40 games played, then the player is deemed injury prone and their statistics are
        almost negligible. 

    Plus, to make this model as accurate as possbile, it is also important to analyze storylines, team chemistry, coaching, etc, 
        which can be considered as a dynamic statistic that is more intuitive but also quantifiable to a decent extent. 

    Finally, some things to also consider adding on as I build this project would be in-season awards like MVP, DPOY, MIP, ROY, and COY. 
        In addition, I could also develop it to the point where it also predicts the playoffs and its award winners. This level would
        have to yet again take into account dynamic statistics mentioned before, as well as factors including home-court advantage and
        level of intensity such as Game 7s and elimination games.

# Gear 3 
    The goal in this gear is to establish all of the foundation for this project using ML. It should be able to take in data, make sense of it, push it into analysis, and build a basic regular season predictor. 

# Gear 4
    Now this is about accounting for NBA players with no stats from the 2025-26 season, who could happen to be rookies, or international and injured players coming back in the 2026-27 after missing last year. The rookies will be addressed using NCAA, international, and G-League stats. All in all, this helps better solidify the predictor by adding more player stats that can drastically influence the standings. 

# 1Q (Gear 5)
    This consists of using Neural Networks to strengthen the predictions and then comparing them to the Ridge model to see which is better, and possibly aim for a combination of both results if the outcomes happen to be similar or there is no clear winner. After this, First-Quarter of NBA Prophet will be done.  

# 2Q (Gear 6)
    Next is the Second-Quarter 2Q(reaching the end of the First-Half), where roster updates need to be automatically updated instead of me running the file everytime and then finally adding the dynamic statistics such as level of coaching adjustments, chemistry, player growth, which I believe can be done with building AI models. After that is when the predictions on the websites will be updated accordingly. This will transition into the Third-Quarter 3Q, where it is more about alteration of the standings based on user input. 

# 3Q (Gear 7)
    (coming soon)

# 4Q (Gear 8)
    (coming soon)

