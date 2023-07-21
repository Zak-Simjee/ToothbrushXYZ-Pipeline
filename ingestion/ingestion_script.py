"""Module to extract toothbrush xyz data for desired day from S3 bucket 
and then produce a data frame which is uploaded to a postgreSQL database"""

from os import environ
from argparse import ArgumentParser, Namespace
from datetime import datetime
from s3fs import S3FileSystem
from dotenv import dotenv_values
import pandas as pd
from sqlalchemy import create_engine

def handler(event, context):

    CURRENT_DATE = datetime.now().strftime("%Y/%m/%d")
    SCHEMA = "week4_zaak_staging"

    def collect_arguments() -> Namespace:
        """Function to collect and parse arguments from command line"""

        desc = """Module to extract toothbrush xyz data for desired day from S3 bucket 
        and then produce a data frame which is uploaded to a postgreSQL database"""

        arguments = ArgumentParser(description=desc)
        arguments.add_argument("-env", help="specify a .env file to use.", default=None)

        return arguments.parse_args()


    def get_tb_data(bucket: str, config: dict, directory: str="/tmp", date: str=CURRENT_DATE) -> pd.DataFrame:
        """Establish connection to S3, download desired data and return data frame of that data"""

        print("Connecting to S3...")
        fs = S3FileSystem(key=config["ACCESS_KEY"], secret=config["SECRET_KEY"])
        path = bucket + "/" + date
        files = fs.ls(path)
        print("S3 Connection Success.")

        print("Downloading data...")
        for file in files:
            fs.download(file, f"{directory}/order_date.csv")
        print("Successfully downloaded Toothbrush XYZ data.")

        return pd.read_csv(f"{directory}/order_date.csv")


    def create_staging_table(df: pd.DataFrame, config: dict) -> None:
        """Establish connection to PostgreSQL database and create table from a given data frame"""

        print("Connecting to database")
        DB_URI = f"postgresql+psycopg2://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
        engine = create_engine(DB_URI)
        print("Database Connection Success.")

        print("Creating staging table...")
        df.to_sql("staging_ecommerce", engine, index=False, schema=SCHEMA, if_exists="replace")
        print("Table successfully created.")


    arguments = collect_arguments()

    if arguments.env:
        config = dotenv_values(f"{arguments.env}")
    else:
        config = environ

    tb_df = get_tb_data("toothbrush-xyz", config)
    create_staging_table(tb_df, config)
