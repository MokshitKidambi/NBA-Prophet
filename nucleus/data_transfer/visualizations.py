import pandas
import matplotlib.pyplot as plt

predictions = pandas.read_csv(
    "nba_prophet_2026_27_predictions.csv"
)

predictions = predictions.sort_values(
    "ADJUSTED_WINS",
    ascending=True
)

plt.figure(figsize=(10, 12))

plt.barh(
    predictions["TEAM_NAME"],
    predictions["ADJUSTED_WINS"]
)

plt.xlabel("Projected Wins")
plt.ylabel("Team")
plt.title("NBA Prophet — 2026–27 Projected Wins")

plt.tight_layout()

plt.savefig(
    "nba_prophet_2026_27_predictions.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()