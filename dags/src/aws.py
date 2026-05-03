from airflow.sdk import ObjectStoragePath
import json
import logging as log
import re
import os
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from src.testing import validation


load_dotenv(find_dotenv(), override=True)

s3_options = {
    "key": os.getenv("AWS_ACCESS_KEY_ID"),
    "secret": os.getenv("AWS_SECRET_ACCESS_KEY")
}


def load_to_s3(data: dict, path: ObjectStoragePath):
    log.info("Loading JSON to S3...")
    try:
        with path.open('w') as f:
            json.dump(data, f)
            log.info(f"JSON was successfully saved to {path}")
    except Exception as e:
        log.error(f"An error occurred while loading to S3 {e}")
        raise

def upload_from_s3(path: ObjectStoragePath):
    try:
        if re.search(r"\bbronze\b", str(path)):
            log.info("Extracting JSON from Bronze Layer...")
            with path.open('r') as f:
                d = json.load(f)
                value = validation(d)
                log.info(f"JSON was successfully extracted from {path}")
                return value
        if re.search(r"\bsilver\b", str(path)):
            log.info("Extracting parquet from Silver Layer...")
            df = pd.read_parquet(
                path = path,
                storage_options = s3_options,
                engine = 'pyarrow',
            )
            return df
    except Exception as e:
        log.error(f"An error occurred while extracting from S3 {e}")
        raise