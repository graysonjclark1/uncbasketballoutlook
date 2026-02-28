from bs4 import BeautifulSoup
import requests
from datetime import date
import pandas as pd
import numpy as np

r = requests.get("https://www.sports-reference.com/cbb/schools/north-carolina/men/2026-schedule.html")
r.raise_for_status()
html = r.text
soup = BeautifulSoup(html, 'html.parser')

rows = soup.select("tbody tr")
today = date.today().isoformat()
games = 0
pts_scored_list = []
pts_against_list = []

for row in rows:
    if "thead" in row.get("class", []):
        break

    date_cell = row.select_one('td[data-stat="date_game"]')
    if not date_cell:
        continue


    csk_value = date_cell.get("csk")
    if csk_value > today:
        break

    games += 1
  
    pts_cell = row.select_one('td[data-stat="pts"]')
    opp_pts_cell = row.select_one('td[data-stat="opp_pts"]')
    srs_cell = row.select_one('td[data-stat="srs"]')

    if not pts_cell or not opp_pts_cell or not srs_cell:
        continue

    pts_txt = pts_cell.get_text(strip=True) if pts_cell else ""
    opp_txt = opp_pts_cell.get_text(strip=True) if opp_pts_cell else ""
    srs_txt = srs_cell.get_text(strip=True) if srs_cell else ""

    try:
        pts_scored_list.append(float(pts_txt))
        pts_against_list.append(float(opp_txt))
    except Exception as e:
        print(row)

season = "2026"
avg_pts_scored = np.mean(pts_scored_list)
avg_pts_against = np.mean(pts_against_list)

data = {
    'Season' : [season],
    'Avg Pts Scored' : [avg_pts_scored],
    'Avg Pts Against' : [avg_pts_against],
    'SRS' : [srs_txt]
}

df = pd.DataFrame(data)



def update_data(num_games, season):
    print(season)
    r = requests.get(f"https://www.sports-reference.com/cbb/schools/north-carolina/men/{season}-schedule.html")
    try:
        r.raise_for_status()
    except Exception as e:
        print(e)
        return
    
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    table_data = soup.find_all("tbody")
    table_data = table_data[1]

    pts_scored_arr = []
    pts_against_arr = []

    rows = soup.select("tbody tr")
    i = 0
    for row in rows:
        if i == 28 or "thead" in row.get("class", []) or "thead rowSum" in row.get("class", []):
            break
        pts_cell = row.select_one('td[data-stat="pts"]')
        opp_pts_cell = row.select_one('td[data-stat="opp_pts"]')
        srs_cell = row.select_one('td[data-stat="srs"]')

        if not pts_cell or not opp_pts_cell or not srs_cell:
            continue

        pts_txt = pts_cell.get_text(strip=True) if pts_cell else ""
        opp_txt = opp_pts_cell.get_text(strip=True) if opp_pts_cell else ""
        srs_txt = srs_cell.get_text(strip=True) if srs_cell else ""

        try:
            pts_scored_arr.append(float(pts_txt))
            pts_against_arr.append(float(opp_txt))
        except Exception as e:
            print(row)

        i += 1
    
    avg_pts_scored = np.mean(pts_scored_arr)
    avg_pts_against = np.mean(pts_against_arr)

    return  pd.DataFrame({
    'Season' : [season],
    'Avg Pts Scored' : [avg_pts_scored],
    'Avg Pts Against' : [avg_pts_against],
    'SRS' : [srs_txt],
    })

seasons = np.arange(2025,2002,-1)
seasons_without_2020 = np.delete(seasons, 5)

for i in range(len(seasons_without_2020)):
    data_attrs = update_data(games, seasons_without_2020[i])
    df = pd.concat([df, data_attrs], ignore_index=True)

print(df)
df.to_csv("final_dataset.csv")