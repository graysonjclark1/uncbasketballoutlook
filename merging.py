import pandas as pd
import numpy as np

old_csv = pd.read_csv("unc_records.csv")[["Season", "NCAA Tournament"]]

old_csv["Season"] = ("20" + old_csv["Season"].str.split("-").str[1]).astype(int)

for i in range(1, len(old_csv)):
    # print(i,"---------")
    # print(old_csv.iloc[i]["NCAA Tournament"])
   if pd.isna(old_csv.iloc[i]["NCAA Tournament"]):
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "Miss Tournament"

   elif old_csv.loc[old_csv.index[i], "NCAA Tournament"] == "Lost NCAA Tournament First Round":
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "First Round"

   elif old_csv.loc[old_csv.index[i], "NCAA Tournament"] == "Lost NCAA Tournament Second Round": 
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "Second Round"

   elif old_csv.loc[old_csv.index[i], "NCAA Tournament"] == "Lost NCAA Tournament Third Round":
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "Sweet Sixteen"


   elif old_csv.loc[old_csv.index[i], "NCAA Tournament"] == "Lost NCAA Tournament Regional Semifinal":
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "Sweet Sixteen"

   elif old_csv.loc[old_csv.index[i], "NCAA Tournament"] == "Lost NCAA Tournament Regional Final":
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "Elite Eight"
   
   elif old_csv.loc[old_csv.index[i], "NCAA Tournament"] == "Lost NCAA Tournament National Semifinal":
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "Final Four"
   
   elif old_csv.loc[old_csv.index[i], "NCAA Tournament"] == "Lost NCAA Tournament National Final":
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "National Runner-Up"
   
   elif old_csv.loc[old_csv.index[i], "NCAA Tournament"] == "Won NCAA Tournament National Final":
      old_csv.loc[old_csv.index[i], "NCAA Tournament"] = "National Champions"

old_csv = old_csv[:24]

new_csv = pd.read_csv("final_dataset.csv")

newest_csv = pd.merge(old_csv, new_csv, on="Season")

newest_csv = newest_csv.drop(columns=["Unnamed: 0"])

newest_csv.to_csv("actual_dataset.csv")