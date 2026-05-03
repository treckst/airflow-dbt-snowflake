import pandas as pd
import logging as log
from airflow.sdk import ObjectStoragePath
import os
from dotenv import load_dotenv, find_dotenv
import re

load_dotenv(find_dotenv(), override=True)
BUCKET_BASE = os.getenv("BUCKET_BASE_PATH")


class Transformation(Exception):
    pass
pd.set_option('display.max_columns', None)

s3_options = {
    "key": os.getenv("AWS_ACCESS_KEY_ID"),
    "secret": os.getenv("AWS_SECRET_ACCESS_KEY")
}

def silver_transform(data, file_date):
    #remove then index_col when reading from api
    try:
        log.info(f"Executing silver transformation...")

        must_have=[
            'symbol', 'open', 'close', 'low',
            'high', 'volume', 'name', 'exchange_code', 'exchange',
            'date', 'price_currency', 'asset_type'
        ]

        df = pd.DataFrame(data['data'], columns=must_have)

        df.drop_duplicates(inplace=True)
        df['date'] = pd.to_datetime(df['date']).dt.date
        parq_path = re.findall(r"(\d{4}-\d{2}-\d{2})", str(data))
        truth = f"{BUCKET_BASE}/silver/{file_date}.parquet"
        df.to_parquet(
            path = truth,
            storage_options = s3_options,
            engine = 'pyarrow',
            index = False,
        )
        log.info(f"Silver transformation successfully completed!.")
        truth_path = ObjectStoragePath(truth)

        return truth_path

    except Exception as e:
        log.error(f"Error occurred during silver transformation: {e}")
        raise
