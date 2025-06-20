import json
import os
import datetime
import logging
import urllib.request

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import boto3
s3 = boto3.client('s3')

# Configuration (make sure these are set in the Lambda environment variables)
S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
CITY_LATITUDE = os.environ.get('CITY_LATITUDE')
CITY_LONGITUDE = os.environ.get('CITY_LONGITUDE')

WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

def lambda_handler(event, context):
    logger.info(f"Lambda function triggered at {datetime.datetime.now()}")

    if not S3_BUCKET_NAME or not CITY_LATITUDE or not CITY_LONGITUDE:
        logger.error("Missing environment variables: S3_BUCKET_NAME, CITY_LATITUDE, or CITY_LONGITUDE.")
        return {
            'statusCode': 500,
            'body': json.dumps('Configuration error: Missing environment variables.')
        }

    try:
        # Build API URL with parameters
        params = (
            f"latitude={CITY_LATITUDE}&longitude={CITY_LONGITUDE}"
            "&current_weather=true"
            "&temperature_unit=fahrenheit"
            "&windspeed_unit=mph"
            "&timezone=auto"
        )
        full_url = f"{WEATHER_API_URL}?{params}"
        logger.info(f"Fetching weather data from: {full_url}")

        with urllib.request.urlopen(full_url) as response:
            weather_data = json.loads(response.read().decode())

        logger.info(f"Weather data: {weather_data}")

        current_weather = weather_data.get('current_weather', {})
        logger.info(f"Current weather: {current_weather}")

        # Parse timestamp safely
        time_value = current_weather.get('time')

        if time_value:
            try:
                # Open-Meteo returns ISO8601 string like "2025-06-20T18:30"
                timestamp = datetime.datetime.fromisoformat(time_value).isoformat()
            except ValueError:
                # If format isn't ISO, assume UNIX timestamp
                timestamp = datetime.datetime.fromtimestamp(float(time_value)).isoformat()
        else:
            timestamp = datetime.datetime.now().isoformat()

        formatted_data = {
            "timestamp": timestamp,
            "latitude": CITY_LATITUDE,
            "longitude": CITY_LONGITUDE,
            "temperature": current_weather.get('temperature'),
            "windspeed": current_weather.get('windspeed'),
            "winddirection": current_weather.get('winddirection'),
            "weathercode": current_weather.get('weathercode'),
            "is_day": current_weather.get('is_day'),
            "source_api": "Open-Meteo"
        }

        current_utc_time = datetime.datetime.utcnow()
        s3_key_prefix = current_utc_time.strftime("data/%Y/%m/%d/")
        s3_file_name = current_utc_time.strftime("weather_%Y-%m-%d-%H-%M-%S.json")
        s3_object_key = s3_key_prefix + s3_file_name
        logger.info(f"Uploading data to S3 key: {s3_object_key}")

        s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=s3_object_key,
            Body=json.dumps(formatted_data, indent=2),
            ContentType='application/json'
        )
        logger.info(f"Successfully uploaded to s3://{S3_BUCKET_NAME}/{s3_object_key}")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Weather data saved to S3 bucket {S3_BUCKET_NAME} as {s3_object_key}!')
        }

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {e}')
        }
