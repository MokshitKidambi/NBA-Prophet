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
    The goal in this gear is to establish all of the foundation for this project, not including the AI/ML stuff. It should be able to take in data, make sense of it, push it into analysis, and build a basic regular season predictor. 

# Gear 4
    Now this is about solidifying the predictor by adding more NBA details and the dynamic statistics to make the model even more
    accurate and well-structured. 

