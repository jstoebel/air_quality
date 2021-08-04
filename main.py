import requests

from models import *
from settings import settings

def main():
    url = f"https://www.airnowapi.org/aq/observation/zipCode/current"

    params = {
        "format": "application/json",
        "zipCode": settings.ZIP_CODE,
        "distance": "50",
        "API_KEY": settings.API_KEY
    }

    res = requests.get(url, params=params)
    results = AirQualityResultsList(results=res.json())
    print(results.report)
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
