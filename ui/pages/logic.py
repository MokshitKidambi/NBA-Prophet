import streamlit as st

st.set_page_config(
    page_title="How NBA Prophet Works",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        display: none;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("How NBA Prophet Works")

st.markdown("*Developed by Mokshit Kidambi*")

st.write(
    """
    NBA Prophet predicts each team's next-season performance using
    historical team performance, roster movement, continuity, and
    availability-related features.
    """
)

st.header("What Data Goes Into the Model")

st.markdown("""
To decide what data would be best to use for the prediction model, I had conducted extensive research 
on the different types of statistics that exist in the NBA. My reasearch can be sectioned into 2 sections: Module 1 and Module 2. 

The former contained team statistics and weighed the capabilities of traditional statistics, shooting efficiency, possession-based statistics,
and possession control.

The latter contained player statistics and focused on analyzing traditional statistics, player efficiency, usage & offensive responsibility, 
advanced impact metrics, on & off impact, and availability.

---

### Feature Selection

Then, at the end of each module, I formatted all gathered statistics into 3 sections: 

- Initial Features
- Might Keep
- Take Out

Which is how I was able to choose which stats to use for the model. 

Things that were considered to make those decisions are the stat's significance, pros and cons, and predictive value.

Thus, I decided to keep the following statistics for the first part of the model:

#### Module 1:

- PPG
- Opponent PPG
- TS%
- Net Rating
- TOV%
- ORB%
- DRB%
- AST Ratio

#### Module 2:

- PPG
- MPG
- TS%
- USG%
- VORP
- GP
- Multi-Season Availability

---

### Gathering and Organizing the Data

After gathering statistics using the NBA's API, I made a folder for unfiltered traditional and advanced statistics, where I also made sub folders for players and teams. would then only keep the ones that are in the initial features list that I made, 
which also required me to derive new stats, such as PPG through a team/player's total points divided by their total games played. 

Then, I took these unfiltered data and modify them to fit the criteria for the prediction model, which was stored in the filtered folder of my data folder and it followed the same behavior as the unfiltered folder. 

Such a process had to be implemented as some of the stats were redundant while others had a fair amount of flaws as benefits. 

---

### Monitoring Roster Changes

However, the most important part in all of this was monitoring roster changes of each team, which was tracked by 3 separate data frames: 

- Returning
- Incoming
- Outgoing

It's methodology is quite simple: Returning are the players who have stayed on the same team in the following season; Incoming are new players added during the off-season or 
regular season via trades; Outgoing are players who left the team in free-agency or those who were traded.

---

### Creating New Statistics

Using these data frames, I created new statistics such as Scoring Load (PPG times MPG), then later expanded to Efficiency, Usage, and Plus Minus Load, and Weighted True Shooting Percentage (TS_PCT times TOTAL_MINS).

Plus, the load statistics were converted to net statistics that displayed the loss or gain for each load statistic following major signings or trades that lead into the upcoming season. 

With the use of these data frames, a team's loss in production versus their gain through other acquisitions were closely monitored, leading to new statistics such as
Scoring Share, which was the result of the scoring load divided by the scoring load of the previous season for the appropriate data frame. 

Like previously, the expansion of this idea led to other shares such as efficiency, usage, and plus minus (which was dropped later because of its low contribution), and then converted to net statistics. 

---

### Core Availability

In addition, it is also important to measure the availability of a team's core, which consists of its eight best players, thus stats such as Core Availability and its standard deviation
were created to measure the availability of those core players during the following season.

---

### Final 13 Features

And after trial and error with the model, these 13 features became the backbone of the model:

- Net Rating
- Team Turnover Percentage
- Defensive Rebound Percentage
- Assist Ratio
- Pace
- Net PPG Change
- Retained Minutes
- Net Scoring Load
- Net Efficiency Load
- Net Usage Load
- Net Plus-Minus Load
- Standard Deviation of Core Availability 
- Returning Scoring Share

Therefore, these were the statistics developed to train the model in predicting the regular season win record for all 30 NBA teams.    
""")

st.header("How the Model Learns")

st.markdown("""
In order to predict the 2026-27 regular season records, I decided that it would be best to train my model on the data of the last 30 NBA seasons, so that each season would predict the record of the following season until the 2025-26 NBA season. 

I used the pandas library sci-kit learn in order to train my prediction model. I started by using common models such as Linear Regression, which gave me a basic but well idea aboutcorrelation between a certain stat and my Y-coordinate, which was the regular season win percentage of the following NBA season.

---

### Evaluating the Model

To quantify my results, I generated 2 columns in my result Data Frame:

- Predicted Wins per 82 (predicted win percentage times 82)
- Absolute Wins per 82 (next season win percentage times 82)

Then, I took the difference of both to get the absolute and predicted errors.

In addition, mean absolute error was a measure that I used to see how far the wins generated by my predicted model were from the actual team wins on average for all teams from that season's standings.

To make sense of the stat, I multiplied it by 82 to get the mean absolute error wins.

Thus, my evaluation of which statistics worked best was based on the lowest amount of mean absolute error wins on average across the 2017-18 to 2023-24 seasons, which are the seven seasons I trained the model on.

The lowest mean absolute error wins reached through the entire training process was 6.776 wins, using the 13 features mentioned before.

---

### Comparison Models

For comparison's sake, I also took:

- A simple mean absolute error, which is based on what would happen if all teams were projected to have a 0.500 win percentage
- A naive mean absolute error, which was on the assumption that teams' win percentage would not change in the following year, regardless of any off-season moves their front office makes.

---

### Feature Refinement

Subsequently, this process led me to try out many different stats where I found out which benefitted the model, and vice versa.

Some previously discussed statistics were removed, such as:

- the efficiency share for the returning players
- the core availability stat (but its standard deviation proved useful)

---

### Model Refinement

Then, I switched up the models from Linear Regression to see if other models produce the same results or not, which led me to try:

- Ridge Regression
- Elastic Net (Lasso Regression)

Which both needed standardization of the features using Standard Scaler.

By doing that, the Ridge Regression proved to be slightly more useful so I switched the model to using Ridge.

Later, I switched up the linear pattern and tried other models such as:

- Random Forest Regressor
- Gradient Boosting Regressor

But none of them provided any benefits, therefore using Ridge as the official model for the prediction engine.

Finally, alongside the projected wins, I also added Roster Confidence and Roster Sensitivity to provide a measure of how trustworthy the predictions are.
""")

st.header("How 2026–27 Predictions Are Made")

st.markdown(
    """
    **2025–26 Team Performance**  
    +  
    **2025–26 → 2026–27 Roster Changes**  
    +  
    **Continuity & Availability Features**  
    ↓  
    **13 Final Features**  
    ↓  
    **StandardScaler**  
    ↓  
    **Ridge Regression**  
    ↓  
    **League Calibration**  
    ↓  
    **Final Projected Wins**
    """
)

st.header("Understanding the Standings")

st.markdown("""
The resulting standings are simple to understand. The 30 NBA teams are divided into the Eastern and Western Conferences, based on their geography, and are ranked from 1 through 15 based on their regular season win totals.

Thus, the engine predicts:

- The **Detroit Pistons** to have the number 1 seed in the **Eastern Conference**
- The **San Antonio Spurs** to have the number 1 seed in the **Western Conference**

Meanwhile, it displays:

- The **Washington Wizards** at the very bottom of the Eastern Conference
- The **Sacramento Kings** at the very bottom of the Western Conference
""")

st.header("Model Limitations")

st.markdown("""
While the model is able to provide these predictions at a high level, there are some significant limitations it faces that stops it from being fully accurate.

First, the model seems to not account for dynamic factors such as:

- Coaching adjustments
- Team chemistry
- Player issues on and off the court
- Etc.

These factors that are all very impactful on the success of an NBA team throughout an 82 game regular season.

---

Second, the emergence of NBA rookies means that there are no available statistics that could measure their impact, which can lead to the predictions being thrown off by a good amount.

---

However, as the model is still in its early stages, it will continued to be improved with the means of surpassing said limitations in the future.
""")

if st.button("← Back to Predictions"):
    st.switch_page("app.py")