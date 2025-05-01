

API_URL = "https://api.taylorsweatherapi.com/?zipcode=37167"

HEADERS = {
    "Content-Type": "application/json",
    "x-api-key": "bTK3tM6Zwj8cHACQtSRH26aEFwzeQ4ns9YInqoj5",
    "Accept": "application/json"
}

def fetch_weather_data(status_display_object, network_client):
    try:
        response = network_client.fetch(API_URL, headers=HEADERS, timeout=30)
        network_client.neo_status(value=(0, 100, 0)) #should set the status LED to green

        data = response.json()

        print("Response:", data)

        if 'current' not in data:
            raise KeyError("API response does not contain weather info")

        status_display_object.text = ""

        return data

    except (ValueError, RuntimeError, KeyError, ConnectionError) as e:
        error_msg = f"Fetch Error: {str(e)}"
        network_client.neo_status(value=(100, 0, 0)) #should set the status LED to red
        status_display_object.text = ""
        print(error_msg) 
        return None