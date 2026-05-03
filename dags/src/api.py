from airflow.sdk import ObjectStoragePath
import requests
import logging as log
import json
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv(), override=True)

API_KEY = os.getenv("M_API_KEY")
tickers = 'NVDA,AAPL,GOOGL,MSFT,AMZN,META,TSLA'



def extract_api(start_date: str, end_date: str):
    try:
        URL = f"https://api.marketstack.com/v2/eod"
        params = {
            'access_key': API_KEY,
            "symbols": tickers,
            'date_from': str(start_date),
            'date_to': str(end_date)
        }
        response = requests.get(URL, params=params)
        response.raise_for_status()
        log.info("API response received successfully")
        data = response.json()
        return data

    except requests.exceptions.RequestException as e:
        log.error(f"An error occured while requesting {e}")
        raise

def load_to_s3(data: dict, path: ObjectStoragePath):
    log.info("Loading JSON to S3...")
    try:
        with path.open('w') as f:
            json.dump(data, f)
    except Exception as e:
        log.error(f"An error occured while loading to S3 {e}")
        raise


