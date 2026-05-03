from airflow.sdk import dag, task, ObjectStoragePath
from pathlib import Path
from pendulum import datetime
from dotenv import load_dotenv, find_dotenv
from airflow.timetables.interval import CronDataIntervalTimetable
from airflow.providers.snowflake.transfers.copy_into_snowflake import CopyFromExternalStageToSnowflakeOperator
from cosmos import ProjectConfig, ProfileConfig, ExecutionConfig, DbtTaskGroup
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

import os

from src.api import extract_api, load_to_s3
from src.aws import upload_from_s3
from src.transform import silver_transform


DBT_PROJECT_PATH = Path("/opt/airflow/dbt/dbt_snowflake_project")


_project_config = ProjectConfig(
    dbt_project_path = DBT_PROJECT_PATH,
    install_dbt_deps=True
)

_profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id='stocks_snowflake',
        profile_args={
            "database": "STOCKS",
            "schema": "SOURCE",
        },
    ),
)

_execution_config = ExecutionConfig(
        dbt_executable_path="/opt/airflow/dbt_venv/bin/dbt", 
    )

load_dotenv(find_dotenv(), override=True)
BUCKET = os.getenv("BUCKET_BASE_PATH")
BUCKET_PATH = ObjectStoragePath(BUCKET, conn_id="aws_default")

@dag(
    schedule=CronDataIntervalTimetable("@weekly", timezone="Europe/Warsaw"),
    start_date=datetime(year=2026, month=3, day=1, tz="Europe/Warsaw"),
    end_date=datetime(year=2026, month=5, day=31, tz="Europe/Warsaw"),
    catchup=True,
    is_paused_upon_creation=True,
    max_active_runs=1
    )

def stocks_elt():

    @task.python
    def extract_to_s3(**kwargs):
        data_interval_start = kwargs['data_interval_start'].strftime('%Y-%m-%d')
        data_interval_end = kwargs['data_interval_end'].strftime('%Y-%m-%d')
        raw_data = extract_api(data_interval_start, data_interval_end)
        bronze_path = BUCKET_PATH / "bronze" / f"{data_interval_end}.json"
        load_to_s3(raw_data, bronze_path)
        return bronze_path

    @task.python
    def as_parquet(path: ObjectStoragePath):
        file_date = path.name.replace('.json', '')
        bronze = upload_from_s3(path)
        silver_path = silver_transform(bronze, file_date)
        return silver_path

    load_to_snowflake = CopyFromExternalStageToSnowflakeOperator(
        task_id="load_to_snowflake",
        snowflake_conn_id="stocks_snowflake",
        files=["{{ data_interval_end | ds }}.parquet"],
        table='STOCKS.SOURCE.RAW',
        stage="STOCKS.SOURCE.my_s3_loading_dock",
        file_format="(type = 'PARQUET')",
        copy_options="MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE"
    )

    first = extract_to_s3()
    second = as_parquet(first)

    cosmos_dag = DbtTaskGroup(
        group_id="dbt_transform",
        project_config= _project_config,
        profile_config= _profile_config,
        execution_config = _execution_config
    )

    second >> load_to_snowflake >> cosmos_dag


stocks_elt()