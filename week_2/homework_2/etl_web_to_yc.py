import boto3
import pandas as pd
from pathlib import Path
from prefect import flow, task

@task(retries=3)
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas DataFrame"""
    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Fix datatype issues"""
    df["lpep_pickup_datetime"] = pd.to_datetime(df["lpep_pickup_datetime"])
    df["lpep_dropoff_datetime"] = pd.to_datetime(df["lpep_dropoff_datetime"])
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df

@task()
def write_local(df_transform: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame out locally as parquet file"""
    path = f"week_2/data/{color}/{dataset_file}.csv"
    df_transform.to_csv(path)
    return path

@task()
def write_yc(path: Path, dataset_file) -> None:
    """Write file to Yandex Cloud Storage"""
    bucket_name = "de-zoomcamp"
    file_name = f"{dataset_file}.csv"
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )

    s3.upload_file(path, "de-zoomcamp", file_name)


@flow()
def etl_web_to_yc():
    """The main ETL function"""
    color = "green"
    year = 2020
    month = "01"

    dataset_file = f"{color}_tripdata_{year}-{month}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_transform = transform(df)
    path = write_local(df_transform, color,dataset_file)
    write_yc(path,dataset_file)


if __name__ == '__main__':
    etl_web_to_yc()
