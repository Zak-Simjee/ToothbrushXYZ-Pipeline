# Dashboard

A web app made using dash to display visualisations for Toothbrush XYZ data. Designed to be used as a local app or can be built into a container with Docker. Web app will default to local host on port 8080. Designed for PostgreSQL database.

## Install

pip3 install requirements.txt

## Usage

python3 app.py

## Containerisation

docker build -t dashboard

## .env

This app requires a .env file in the root directory in the format:

DB_HOST=["Endpoint/URL for Database"]

DB_USER=["Username to access Database"]

DB_PASS=["Username to access Database"]

DB_NAME=["Name of Database"]

DB_PORT=["Port of Database"]
