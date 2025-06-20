# aws_serverless_data_weather_fetcher
Fetches weather data from Open-Meteo for New Delhi and stores it in an S3 bucket in structured JSON format.


## Project Overview

This project demonstrates a basic serverless data ingestion pipeline built on AWS. It automatically fetches current weather data from a public API, processes it, and stores it as historical records in an Amazon S3 bucket. This showcases fundamental cloud skills including serverless compute (AWS Lambda), scalable storage (AWS S3), and scheduled automation (AWS EventBridge).

## Architecture

![image](https://github.com/user-attachments/assets/60750166-c3d2-4de1-b269-27691256752a)


## Key AWS Services Used

* **Amazon S3 (Simple Storage Service):** Used as a highly durable, scalable, and secure storage for the raw and processed weather data.
* **AWS Lambda:** A serverless compute service that runs the Python code to fetch and store data without managing any servers.
* **AWS IAM (Identity and Access Management):** Configured to provide the Lambda function with the necessary permissions to write objects to the S3 bucket and log to CloudWatch.
* **AWS EventBridge:** Used to set up a scheduled rule that triggers the Lambda function periodically (e.g., daily).
* **AWS CloudWatch:** For monitoring Lambda function invocations, duration, errors, and logs.

## Data Source

* **Open-Meteo API:** A free and open-source weather API used to fetch real-time weather information. No API key is typically required for basic usage.
    * API URL: `https://api.open-meteo.com/v1/forecast`
    * Documentation: [https://open-meteo.com/](https://open-meteo.com/)

**Prerequisites:**
* An active AWS Account (ensure you are mindful of [AWS Free Tier limits](https://aws.amazon.com/free/)).
* Basic familiarity with the AWS Management Console.
