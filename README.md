# *Stocks ELT Pipeline: Airflow, Snowflake & dbt*
<img width="1946" height="1147" alt="Untitled scene" src="https://github.com/user-attachments/assets/27714572-f2f0-4020-b53e-00c6a02a0a0c" />


## This project is an end-to-end pipeline that extracts weekly stock market data, processes it through a data lake (AWS S3), loads it into a cloud data warehouse (Snowflake), and models it using Dbt Core for business intelligence (Power BI).
## Everything is orchestrated with Apache Airflow using Cosmos by Astronomer for seamless dbt integration which makes each dbt model with test as a separate task instead of hardcoding "dbt run".


##  Architecture & Data Flow

### Extract:
A Python task calls [Stock Prices API](https://marketstack.com/?utm_source=Github&utm_medium=Referral&utm_campaign=Public-apis-repo-Best-sellers) to fetch weekly stock data and lands the raw .json payload into an AWS S3 bucket using Airflow's native ObjectStoragePath.

### Transform to Parquet:
A second Python task reads raw json using Pandas and loads it back to S3 as highly compressed, columnar .parquet file.

### Load to Snowflake:
The CopyFromExternalStageToSnowflakeOperator loads the Parquet data from an S3 directly into the STOCKS.SOURCE.RAW table in Snowflake using COPY INTO with External stage.

### Data Modeling (dbt & [Cosmos](https://github.com/astronomer/astronomer-cosmos)):
Once the raw data is in Snowflake, dbt (core) takes over to transform the raw data into a dimensional Star Schema.

### BI:
The final modeled tables in Snowflake are connected directly to Power BI to power interactive dashboards and reporting.

<img width="1327" height="763" alt="image" src="https://github.com/user-attachments/assets/40900b06-2db5-410c-a99f-944262156b34" />


## Key Features
Instead of running dbt as a single command (dbt run) which would look like a single task in airflow, this project uses [Astronomer Cosmos](https://github.com/astronomer/astronomer-cosmos) (DbtTaskGroup).
Cosmos dynamically parses dbt_project.yml and translates every single dbt model and dbt test into its own native Airflow task.
This provides detailed tracking directly within the Airflow. If a specific data test or model fails, only that specific node fails, making debugging incredibly fast and visual.

<img width="1836" height="682" alt="Zrzut ekranu 2026-05-03 125341" src="https://github.com/user-attachments/assets/e7ffb45d-9c80-41ef-9ad5-a2b714389b3f" />
<img width="1905" height="906" alt="Zrzut ekranu 2026-05-03 125247" src="https://github.com/user-attachments/assets/8f0f0d62-4c97-4a0f-8644-c98eda6476a6" />


# Tech Stack
## Orchestration: Apache Airflow 3.2 (using the new TaskFlow API & Object Storage features)
## Data Lake: Amazon S3
## Data Warehouse: Snowflake
## Transformations: Python (Pandas) & SQL (dbt)
## dbt-Airflow Integration: Astronomer Cosmos
## Visualization: Power BI

# Resources & Inspiration

Building this pipeline involved a lot of learning. Here are the main resources I referenced:

[https://youtu.be/IiczxlbQb8s?si=YyChHtxd-MGaJPe](https://youtu.be/IiczxlbQb8s?si=-jwRWfBx_XX3SLp9), [https://youtu.be/PbSIVDou17Q?si=dPH4WitHZOCBdatS](https://youtu.be/PbSIVDou17Q?si=PscJEFV2aCqR3nOX),
https://youtu.be/vMgFadPxOLk?si=nTcNLE7BW8VO6pfr, https://youtu.be/B8uwFmVt4sU?si=baCpVYRbb9BsDqi, https://youtu.be/9PxRPulvLCg?si=OK4aTys6sRCvF1dT,
https://youtu.be/3SZSDKEZqoA?si=y_O5EWS6Vhj_SFr1

* Cosmos: https://youtu.be/DzxtCxi4YaA?si=ufwffeyWnZFMZrbB, https://youtu.be/iHqtFkm_3i4?si=UallGq-YUiJMExFA, https://youtu.be/zVo8Mv_i2Z8?si=HmBgZsmvoksEBcIo
