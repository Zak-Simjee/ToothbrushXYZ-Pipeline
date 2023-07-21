# Ingestion

A script made to retrieve data for Toothbrush XYZ from an S3 Bucket and upload it to a database. Designed for PostgreSQL database. Can be used locally or built into a container with Docker.

## Install

pip3 install requirements.txt

## Usage

python3 ingestion_script.py

## Containerisation

docker build . -t ingestion

## .env

This app requires a .env file in the root directory in the format:

ACCESS_KEY=["AWS Access Key ID"]

SECRET_KEY=["AWS Secret Key"]

DB_HOST=["Endpoint/URL for Database"]

DB_USER=["Username to access Database"]

DB_PASS=["Username to access Database"]

DB_NAME=["Name of Database"]

DB_PORT=["Port of Database"]
