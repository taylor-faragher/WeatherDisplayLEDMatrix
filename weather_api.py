import requests

API_URL = "https://api.taylorsweatherapi.com/?zipcode=37167"

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": "bTK3tM6Zwj8cHACQtSRH26aEFwzeQ4ns9YInqoj5",
    "Accept": "application/json"
}

def fetch_weather_data():
    try:
        print("Begin fetch")
        response = requests.get(API_URL, headers=HEADERS, timeout=30)
        print("Fetch complete")

        data = response.json()
        print("Data retrieved:", data)

        if 'current' not in data:
            raise KeyError("API response does not contain weather info")

        return data

    except (ValueError, RuntimeError, KeyError, requests.RequestException) as e:
        error_msg = f"Fetch Error: {str(e)}"
        print("Error in weather api:", error_msg)
        return None
