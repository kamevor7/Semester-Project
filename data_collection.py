import os
import requests
import pandas as pd
import json
from datetime import datetime

# API Config
API_KEY = '7fa2ed5284be4e7d9e1ded147195e279'
BASE_URL = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
SERIES_IDS = ['CES0000000001', 'LNS14000000', 'LNS11000000', 'LNS12000000', 'LNS13000000']
DATA_FILE = 'dataset.csv'

# Data fetching for different Series, up to 5 years from the API
def fetch_data(series_id):
    headers = {'Content-type': 'application/json'}
    data = json.dumps({
        "seriesid": [series_id],
        "startyear": str(datetime.now().year - 5),
        "endyear": str(datetime.now().year),
        "registrationkey": API_KEY
    })
    response = requests.post(BASE_URL, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

# Process and Structure the response from the API
def parse_data(response, series_id):
    # Data points initialization
    data_points = []
    for series in response['Results']['series']:
        if series['seriesID'] == series_id:
            for item in series['data']:
                data_points.append({
                    'series_id': series_id,
                    'date': f"{item['year']}-{item['period'][1:]}",
                    'value': float(item['value'])
                })
    return data_points

# Saving Data do CSV File
def save_data_to_csv(data):
    df = pd.DataFrame(data)
    if not os.path.exists(DATA_FILE):
        df.to_csv(DATA_FILE, index=False)
    else:
        existing_data = pd.read_csv(DATA_FILE)
        updated_data = pd.concat([existing_data, df]).drop_duplicates()
        updated_data.to_csv(DATA_FILE, index=False)

if __name__ == "__main__":
    all_data = []
    for series_id in SERIES_IDS:
        response = fetch_data(series_id)
        all_data.extend(parse_data(response, series_id))
    save_data_to_csv(all_data)
    print("Data updated successfully.")
