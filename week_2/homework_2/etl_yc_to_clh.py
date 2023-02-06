import boto3
import pandas as pd
from pathlib import Path
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3,cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1) )
def extract(dataset_url: str, color: str, dataset_file: str) -> pd.DataFrame:
    """Extract csv file and load to Yandex Cloud Storage"""
    df = pd.read_csv(dataset_url)
    return df


@task(log_prints=True)
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write convert dataframe to parquet and save localy"""
    path = f"week_2/data/{color}/{dataset_file}.parquet"
    df.to_parquet(path, compression="gzip")
    return path


@task(log_prints=True)
def write_yc(bucket_name: str, path: Path, dataset_file: str) -> None:
    """Write parquete file to Yandex cloud storage"""
    file_name = f"{dataset_file}.parquet"
    session = boto3.session.Session()
    s3 = session.client(
        service_name="s3", endpoint_url="https://storage.yandexcloud.net"
    )
    s3.upload_file(path, bucket_name, file_name)


@flow()
def etl_yc_to_clh(year: int, month: str, color: str) -> None:
    """Main ETL function"""
    bucket_name = "de-zoomcamp"
    dataset_file = f"{color}_tripdata_{year}-{month}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = extract(dataset_url, color, dataset_file)
    path = write_local(df, color, dataset_file)
    write_yc(bucket_name, path, dataset_file)
    # load_to_cl(bucket_name, path, dataset_file)

@flow()
def etl_parent_flow(months: list[str] = ["02","03"], year: int = 2020, color: str = "yellow"):
    for month in months:
        etl_yc_to_clh(year,month, color)

    


if __name__ == "__main__":
    color = "yellow"
    months = ["02", "03"]
    year = 2020
    etl_parent_flow(months, year, color)
