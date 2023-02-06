# Second homework for workflow orcestration

## Creating virtual environment
 - Create venv with command Python3 -m venv venv
 - Activate venv with command source/venv/bin/activate
 - Install all dependencies pip install -r requirements.txt


 ## Executing scripts
  - elt_web_to_yc.py
     extract data from web and save csf file in Yandex Cloud Storage
  - elt_yc_to_clh.py
     extract data from web, save parquete file localy and then load to Yandex Cloud Storage
     then load data in ClickHouse

     For working with YCS i'am using module boto3 and clickhouse-driver
