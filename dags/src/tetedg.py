import requests
import pandas as pd
import logging as log
from dotenv import load_dotenv, find_dotenv
import os

# Load the environment variables from that specific path
load_dotenv(find_dotenv(), override=True)

API_KEY = os.getenv("M_API_KEY")
tickers = 'NVDA,AAPL,GOOGL,MSFT,AMZN,META,TSLA'


URL = f"https://api.marketstack.com/v2/eod"
params = {
    'access_key': API_KEY,
    "symbols": 'AAPL',
    'date_from': '2026-04-06',
    'date_to': '2026-04-11'
}

def extract_api():
    log.info("Fetching data from API...")
    try:
        response = requests.get(URL, params=params)
        response.raise_for_status()
        log.info("API response received successfully")
        data = response.json()
        df = pd.DataFrame(data['data'])
        df.to_excel('dataaaa.xlsx')
    except requests.exceptions.RequestException as e:
        log.error(f"An error occured while requesting {e}")
        raise

extract_api()