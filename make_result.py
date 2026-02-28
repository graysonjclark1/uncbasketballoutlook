import json
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("actual_dataset.csv")

tourney_map = {
    "Miss Tournament": 0,
    "First Round": 1,
    "Second Round": 2,
    "Sweet Sixteen": 3,
    "Elite Eight": 4,
    "Final Four": 5,
    "National Runner-Up": 6,
    "National Champions": 7
}

features = [
    "Avg Pts Scored",
    "Avg Pts Against",
    "SRS"
]

df["tourney_encoded"] = df["NCAA Tournament"].map(tourney_map)

X = df[features]
y = df["tourney_encoded"]

X = X[1:]
y = y[1:]


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_2025 = X_scaled[-1].reshape(1, -1)

rf = RandomForestClassifier(
    n_estimators=200,
    max_depth=3,
    random_state=42
)

rf.fit(X_scaled, y)
reverse_tourney_map = {v: k for k, v in tourney_map.items()}

predicted_class = rf.predict(X_2025)[0]
predicted_label = reverse_tourney_map.get(predicted_class, "Unknown")


result = {"season": "2025-26", "prediction": predicted_label}

with open("docs/result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)
print("Wrote docs/result.json")

