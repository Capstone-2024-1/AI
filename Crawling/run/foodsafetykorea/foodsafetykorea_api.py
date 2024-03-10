import os

import requests
import pandas as pd

BASE_URL = "http://openapi.foodsafetykorea.go.kr/api"
KEY = "sample"
SERVICE = "COOKRCP01"
TYPE = "json"
n = 50

def fetch_data(start_idx, end_idx):
    url = f"{BASE_URL}/{KEY}/{SERVICE}/{TYPE}/{start_idx}/{end_idx}"
    response = requests.get(url)
    data = response.json()
    return data

data_list = []

start = 1
while True:
    end = start + n - 1
    data = fetch_data(start, end)

    try:
        items = data['COOKRCP01']['row']
        if not items:
            break
        for item in items:
            data_list.append({
                'RCP_SEQ': item['RCP_SEQ'],
                'RCP_NM': item['RCP_NM'],
                'RCP_PARTS_DTLS': item['RCP_PARTS_DTLS']
            })
        start += n
    except KeyError:
        print(f"Finished fetching data or no more data available.")
        break

df = pd.DataFrame(data_list)
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = f"{current_dir}/data/recipes.csv"
df.to_csv(file_path, index=False)

print("Data has been successfully saved to 'recipes.csv'")
