FROM apache/airflow:3.2.0

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

RUN python -m venv /opt/airflow/dbt_venv && \
    /opt/airflow/dbt_venv/bin/pip install --no-cache-dir "dbt-core>=1.11.8" "dbt-snowflake>=1.11.4"