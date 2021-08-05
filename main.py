import requests

from db import AirQualityResult as AirQualityResultDb
from schemas import AirQualityResultsList, CategoryNumber
from settings import settings


def main():
    url = f"https://www.airnowapi.org/aq/observation/zipCode/current"

    params = {
        "format": "application/json",
        "zipCode": settings.ZIP_CODE,
        "distance": "50",
        "API_KEY": settings.API_KEY,
    }

    # res = requests.get(url, params=params)
    # payload = res.json()
    payload = [
        {
            "DateObserved": "2021-08-05 ",
            "HourObserved": 10,
            "LocalTimeZone": "EST",
            "ReportingArea": "Lexington",
            "StateCode": "KY",
            "Latitude": 38.0491,
            "Longitude": -84.4999,
            "ParameterName": "O3",
            "AQI": 30,
            "Category": {"Number": 1, "Name": "Good"},
        },
        {
            "DateObserved": "2021-08-05 ",
            "HourObserved": 10,
            "LocalTimeZone": "EST",
            "ReportingArea": "Lexington",
            "StateCode": "KY",
            "Latitude": 38.0491,
            "Longitude": -84.4999,
            "ParameterName": "PM2.5",
            "AQI": 56,
            "Category": {"Number": 2, "Name": "Moderate"},
        },
    ]
    results_list = AirQualityResultsList(results=payload)

    records = [
        AirQualityResultDb(
            parameter_name=result.parameter_name,
            observation_date_time=result.observation_date_time,
            level=result.category_number,
        )
        for result in results_list.results
    ]

    AirQualityResultDb.bulk_create(records)
    print(results_list.report)

    # if
    #  - any results are moderate or higher
    #  - any results are higher than the current highest for the day
    # send_to_webhook(results.report)
    # if not results.is_healthy:
    #     pass


def send_to_webhook(message):
    url = f"https://maker.ifttt.com/trigger/{settings.IFTTT_EVENT_NAME}/with/key/{settings.IFTTT_WEBHOOK_KEY}"

    res = requests.post(url, json={"value1": message})
    print(f"sending {message}")
    res.raise_for_status()


if __name__ == "__main__":
    main()
