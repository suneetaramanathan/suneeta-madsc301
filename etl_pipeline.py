import requests
import pandas as pd
from sqlalchemy import create_engine
from pymongo import MongoClient
import os

# --------------------------
# STEP 1: FETCH DATA FROM API
# --------------------------
API_KEY = '6e4cb61c-c62c-4e25-b614-217777d3fdc1'
api_url = "http://api.airvisual.com/v2/city"
params = {
    'city': 'Los Angeles',
    'state': 'California',
    'country': 'USA',
    'key': API_KEY
}
response = requests.get(api_url, params=params)
data = response.json()

if data['status'] == 'success':
    pollution_data = data['data']['current']['pollution']
    weather_data = data['data']['current']['weather']
    location_data = {
        'city': data['data']['city'],
        'state': data['data']['state'],
        'country': data['data']['country']
    }
    combined = {**location_data, **pollution_data, **weather_data}
    df_api = pd.DataFrame([combined])
    df_api.rename(columns={'aqius': 'AQI_US', 'mainus': 'Main_Pollutant'}, inplace=True)
else:
    df_api = pd.DataFrame()

# --------------------------
# STEP 2: LOAD AND CLEAN KAGGLE DATA
# --------------------------
df_excel = pd.read_csv("global_air_quality_data_10000.csv")
df_excel.rename(columns={'PM2.5': 'PM2_5', 'Wind Speed': 'Wind_Speed'}, inplace=True)
df_excel['Date'] = pd.to_datetime(df_excel['Date'], errors='coerce')
df_excel.dropna(subset=['PM2_5', 'Date'], inplace=True)
df_excel['Country'] = df_excel['Country'].str.strip().str.title()
df_excel['City'] = df_excel['City'].str.strip().str.title()
df_excel.reset_index(drop=True, inplace=True)

# --------------------------
# STEP 3: CLEAN API DATA
# --------------------------
if not df_api.empty:
    df_api_cleaned = df_api.loc[:, [
        'city', 'state', 'country', 'ts', 'AQI_US', 'Main_Pollutant',
        'tp', 'hu', 'ws'
    ]].copy()

    df_api_cleaned.rename(columns={
        'tp': 'Temperature',
        'hu': 'Humidity',
        'ws': 'Wind_Speed',
        'ts': 'Timestamp',
        'city': 'City',
        'state': 'State',
        'country': 'Country'
    }, inplace=True)
else:
    df_api_cleaned = pd.DataFrame()

# --------------------------
# STEP 4: SAVE TO POSTGRESQL
# --------------------------
try:
    pg_user = 'postgres'
    pg_password = 'admin'
    pg_host = 'localhost'
    pg_port = '5432'
    pg_db = 'air_quality'
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}')
    df_excel.to_sql('historical_air_quality', engine, if_exists='replace', index=False)
    if not df_api_cleaned.empty:
        df_api_cleaned.to_sql('live_air_quality', engine, if_exists='replace', index=False)
except Exception as e:
    print("PostgreSQL error:", e)

# --------------------------
# STEP 5: SAVE TO MONGODB
# --------------------------
try:
    mongo_uri = "mongodb+srv://admin:admin@cluster0.wdmmjjj.mongodb.net/"
    client = MongoClient(mongo_uri)
    db = client["air_quality_db"]
    db["historical_air_quality"].delete_many({})
    db["historical_air_quality"].insert_many(df_excel.to_dict(orient='records'))
    if not df_api_cleaned.empty:
        db["live_air_quality"].delete_many({})
        db["live_air_quality"].insert_many(df_api_cleaned.to_dict(orient='records'))
except Exception as e:
    print("MongoDB error:", e)

# --------------------------
# STEP 6: OPTIONAL FILE SAVE
# --------------------------
os.makedirs("data/processed", exist_ok=True)
df_excel.to_csv("data/processed/historical_air_quality.csv", index=False)
if not df_api_cleaned.empty:
    df_api_cleaned.to_csv("data/processed/live_air_quality.csv", index=False)
