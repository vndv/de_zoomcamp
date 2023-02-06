# Homework for ingest data

## Creating virtual environment
 - Create venv with command Python3 -m venv venv
 - Activate venv with command source/venv/bin/activate
 - Install all dependencies pip install -r requirements.txt

## Running PostgreSQL in Docker

  docker run -it \ 
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:13

## Start ingest data with python script
   
   python script running localy not in docker container

   URL_TRIP="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz"
   URL_LOOKUP="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv" 

   python load_data.py \
   --user root \
   --password root \
   --host localhost \
   --port 5432 \
   --db ny_taxi \
   --url_trip=$(URL_TRIP) \
   --url_lookup=$(URL_LOOKUP)
 