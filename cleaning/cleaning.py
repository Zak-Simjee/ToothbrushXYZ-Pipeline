"""Module to connect to staging database, get staging data, clean it and upload clean data to production database"""

from os import environ
from datetime import datetime, date, timedelta, time, timezone
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, Engine


def handler(event, context):

    STAGING_SCHEMA = "week4_zaak_staging"
    PRODUCTION_SCHEMA = "week4_zaak_production"
    CURRENT_UTC_TIME = datetime.now(timezone.utc).time()
    DATA_UPDATE_TIME = time(13, 5, 0, 0)
    DATA_DATE = date.today() if CURRENT_UTC_TIME > DATA_UPDATE_TIME  else date.today() - timedelta(1)

    def get_db_engine(config: dict) -> Engine:
        """Connect to PostgreSQL database by genereating an sqlalchemy engine with a URI string for the database."""

        DB_URI = f"postgresql+psycopg2://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}"
        return create_engine(DB_URI)


    def clean_tb_data(df: pd.DataFrame) -> pd.DataFrame:
        df["Delivery Status"] = df["Delivery Status"].apply(lambda x: "Not Dispatched" if pd.isnull(x) else x)
        df["Delivery Postcode"] = df["Delivery Postcode"].apply(lambda x: x.replace("%20", " "))
        df["Billing Postcode"] = df["Billing Postcode"].apply(lambda x: x.replace("%20", " "))
        df = df[df["Customer Age"].between(10, 100)]
        df = df[df["Order Date"].dt.date == DATA_DATE]
        df = df.rename(mapper=lambda x: x.lower().replace(" ", "_"), axis=1)
        return df

    load_dotenv()

    print("Loading environment variables...")
    config = environ

    print("Connecting to database...")
    engine = get_db_engine(config)
    print("Connection Success")

    print("Getting staging data...")
    tb_data = pd.read_sql_table("staging_ecommerce", engine,
                                schema=STAGING_SCHEMA, 
                                parse_dates=["Order Date", "Dispatched Date", "Delivery Date"])

    print("Cleaning staging data...")
    tb_data = clean_tb_data(tb_data)

    print("Uploading clean data to Production...")
    tb_data.to_sql("production_ecommerce", engine, 
                    schema=PRODUCTION_SCHEMA, if_exists="replace", 
                    index=False)
    print("Upload Success")
