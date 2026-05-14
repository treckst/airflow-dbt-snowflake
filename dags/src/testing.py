import requests
import pandas as pd
import os
import logging as log
from dotenv import load_dotenv, find_dotenv

class MissingDataError(Exception):
    pass

# Load the environment variables from that specific path
load_dotenv(find_dotenv(), override=True)

API_KEY = os.getenv("M_API_KEY")
tickers = 'NVDA,AAPL,GOOGL,MSFT,AMZN,META,TSLA'

URL = f"https://api.marketstack.com/v2/eod/latest"
params = {
    'access_key':API_KEY,
    "symbols": tickers
}

def extract_api():
    log.info("Fetching data from API...")
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        log.info("API response received successfully")
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        log.error(f"An error occured while requesting {e}")
        raise


def validation(data_dict):
    try:
        api_data = data_dict.get('data', [])
        expected_keys = set(tickers.split(','))
        keys = {row.get('symbol') for row in api_data if 'symbol' in row}
        missing_keys = expected_keys - keys
        if missing_keys:
            raise MissingDataError(f"Missing values for symbol column: {missing_keys}")
        log.info("Successfully validated data")
        return data_dict
    except Exception as e:
        log.error(f"An error occurred while validating {e}")
        raise