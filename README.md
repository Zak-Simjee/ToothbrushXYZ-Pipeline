# Toothbrush Pipeline

This repository contains code designed to read data from a specific S3 Bucket and then pass that data through a cloud hosted data pipeline on AWS finally displaying the results on a dashboard. Each script comes with a Dockerfile and should be dockerised before being hosted on AWS. Ingestion and Cleaning are designed for use with AWS Lambda and Dashboard is designed for EC2 or Fargate.

## Installation

Each folder comes with it's own requirements.txt for use locally or with Docker as well as instructions containted in a README.md file.

## Usage

Once each script has been dockerised and hosted on AWS, the Lambda scripts must be run using either the AWS Lambda test function or can be set to run on an event trigger. The dashboard should be constantly running on an EC2 instance or as a Fargate service.
