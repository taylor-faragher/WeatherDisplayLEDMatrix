# SPDX-FileCopyrightText: 2024 Trevor Beaton for Adafruit Industries
#
# SPDX-License-Identifier: MIT

import http.client
import time
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

# --- Display setup ---
matrixportal = MatrixPortal(width=64, height=32, bit_depth=6, debug=True)

# Create a label for the temperature
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(33, 24),  # Positioned on the right side, near the bottom
    scrolling=False,
)

# Create a label for the weather condition
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(33, 8),  # Positioned on the right side, above the temperature
    scrolling=False,
)

# Dictionary mapping weather conditions to BMP filenames
WEATHER_IMAGES = {
    "Sunny": "images/sunny.bmp",
    "Clear": "images/moon.bmp",
    "Cldy": "images/cloudy.bmp",  # Updated to use shortened version
    "Drizzle": "images/rain.bmp",
    "Rainy": "images/cloudy.bmp",
    "Heavy rain": "images/rain.bmp",
    "TStorms": "images/thunder.bmp",
    "Sun showers": "images/rain.bmp",
    "Snow": "images/snow.bmp",
}

# Update this to your weather feed
UPDATE_DELAY = 1800  # 30 minutes


def get_last_data():
    host = "api.taylorsweatherapi.com"
    endpoint = "/?zipcode=37167"
    try:
        # api_key = "bTK3tM6Zwj8cHACQtSRH26aEFwzeQ4ns9YInqoj5"
        # base_url = "https://api.taylorsweatherapi.com/?zipcode=37167"
        # params = {
        #     "x-api-key": api_key,
        # }
        conn = http.client.HTTPSConnection(host)
        conn.request("GET", endpoint)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        conn.close()
        return data
    except (KeyError, IndexError) as e:
        print(f"Error fetching data: {e}")
        return None


def is_daytime(hour):
    return 5 <= hour < 18  # True if between 5:00 AM and 5:59 PM


def clean_condition(condition, is_day):
    condition = condition.replace("Mostly ", "").replace("Partly ", "")
    condition_mapping = {
        "Cloudy": "Cldy",  # Added shortened version of Cloudy
        "Drizzle or light rain": "Rainy",
        "Heavy rain": "Rainy",
        "Isolated thunderstorms": "TStorms",
        "Sun showers": "Rainy",
        "Scattered thunderstorms": "TStorms",
        "Strong storms": "TStorms",
        "Light snow": "Snow",
        "Heavy snow": "Snow",
    }
    if condition == "Sunny" and not is_day:
        return "Clear"
    return condition_mapping.get(condition, condition)


def parse_weather_data(data):
    try:
        _, weather_info = data.split(" at ")
        time_str, weather_data = weather_info.split(" ", 1)
        hour = int(time_str.split(":")[0])
        if "PM" in time_str and hour != 12:
            hour += 12
        elif "AM" in time_str and hour == 12:
            hour = 0
        temperature, condition = weather_data.split(" and ")
        return hour, temperature, condition
    except ValueError as e:
        print(f"Error parsing weather data: {e}")
        return None, None, None


def update_display():
    weather_data = get_last_data()
    print("weather_data", weather_data)
    # if weather_data:
    # hour, temperature, condition = parse_weather_data(weather_data)
    #     if hour is not None and temperature is not None and condition is not None:
    #         is_day = is_daytime(hour)
    #         current_condition = clean_condition(condition, is_day)

    matrixportal.set_text("70", 0)
    matrixportal.set_text("sunny", 1)

    #         # Determine which image to show based on condition and time
    #         if current_condition == "Sunny" and is_day:
    #             image_key = "images/sunny.bmp"
    #         elif current_condition == "Sunny" and not is_day:
    #             image_key = "images/moon.bmp"
    #         else:
    #             image_key = WEATHER_IMAGES.get(current_condition, "images/sunny.bmp")

    #         try:
    matrixportal.set_background("images/sunny.bmp")
    #         except OSError as e:
    #             print(f"Error loading image for {current_condition}: {e}")
    #     else:
    #         print(f"Failed to parse weather data: {weather_data}")
    #         matrixportal.set_text("Error", 0)
    #         matrixportal.set_text("", 1)
    # print("Failed to retrieve data from feed")
    # matrixportal.set_text("No Data", 0)
    # matrixportal.set_text("", 1)
    # else:
    #     matrixportal.set_text("error", 0)


last_update = time.monotonic()
update_display()

# Main loop
while True:
    current_time = time.monotonic()
    if current_time - last_update > UPDATE_DELAY:
        update_display()
        last_update = current_time

    time.sleep(1)  # Sleep for 1 second
