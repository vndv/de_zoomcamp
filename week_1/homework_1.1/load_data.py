#!/usr/bin/env python
# coding: utf-8

import os
import argparse
import pandas as pd
from sqlalchemy import create_engine
from time import time


def main(params):
    """Main function for extract and load data"""
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    url_trip = params.url_trip
    url_lookup = params.url_lookup


    csv_trip_data = "green_tripdata.csv.gz"
    csv_zone_lookup = "zone_lookup.csv"
    
    #load data from source
    os.system(f"wget {url_trip} -O {csv_trip_data}")
    os.system(f"wget {url_lookup} -O {csv_zone_lookup}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    
    #create zone_lookup dataframe
    df_zone_lookup = pd.read_csv(csv_zone_lookup)
    
    #create table zone_lookup and load data to database
    df_zone_lookup.head(n=0).to_sql(name="zone_lookup", con=engine, if_exists="replace")
    df_zone_lookup.to_sql(name="zone_lookup", con=engine, if_exists="append")
    
    #create iterator for trip data
    df_iter = pd.read_csv(csv_trip_data, iterator=True, chunksize=100000)
    df_trip_data = next(df_iter)
    
    #change colum datatype
    df_trip_data["lpep_pickup_datetime"] = pd.to_datetime(
        df_trip_data["lpep_pickup_datetime"]
    )
    df_trip_data["lpep_dropoff_datetime"] = pd.to_datetime(
        df_trip_data["lpep_dropoff_datetime"]
    )
    
    #create green_trip_data_table and load data to database
    df_trip_data.head(n=0).to_sql(
        name="green_trip_data", con=engine, if_exists="replace"
    )
    df_trip_data.to_sql(name="green_trip_data", con=engine, if_exists="append")

    while True:
        try:
            t_start = time()
            df_trip_data = next(df_iter)
            df_trip_data["lpep_pickup_datetime"] = pd.to_datetime(
                df_trip_data["lpep_pickup_datetime"]
            )
            df_trip_data["lpep_dropoff_datetime"] = pd.to_datetime(
                df_trip_data["lpep_dropoff_datetime"]
            )
            df_trip_data.to_sql("green_trip_data", con=engine, if_exists="append")
            t_end = time()
            print("inserted next chunck.. %.3f seconds" % (t_end - t_start))
        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", required=True, help="user name for postgres")
    parser.add_argument("--password", required=True, help="password for postgres")
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument("--db", required=True, help="database name for postgres")
    parser.add_argument("--url_trip", required=True, help="link for load data")
    parser.add_argument("--url_lookup", required=True, help="link for load data")
    args = parser.parse_args()

    main(args)
