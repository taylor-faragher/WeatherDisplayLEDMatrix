import time
import requests
from PIL import Image, ImageDraw, ImageFont
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from weather_api import fetch_weather_data
from get_temp_color import get_temp_color
from weather_config import get_clean_description, get_image_path, get_x_offset

FETCH_INTERVAL_SECONDS = 900  # 15 minutes

# --- Display setup ---
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # or 'regular' depending on your HAT

matrix = RGBMatrix(options=options)

# Use the default font
font = ImageFont.load_default()

def draw_text(draw, text, pos, color, font):
    draw.text(pos, text, fill=color, font=font)

def load_weather_image(condition):
    if condition == "none":
        return None
    image_path = get_image_path(condition)
    try:
        img = Image.open(image_path).convert("RGB")
        img = img.resize((32, 32))
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def main():
    global_temperature = ""
    global_description = ""
    global_high_temp = ""
    global_low_temp = ""
    global_wind_speed = ""

    while True:
        # Create a blank image for drawing.
        image = Image.new("RGB", (64, 32))
        draw = ImageDraw.Draw(image)

        # Fetch weather data
        try:
            weather_data = fetch_weather_data()
        except Exception as e:
            print(f"Error fetching weather: {e}")
            weather_data = None

        if weather_data:
            current = weather_data['current']
            temperature = current['temperature']
            icon = current['icon']
            min_temp = current['minTemperature']
            max_temp = current['maxTemperature']
            wind_speed = current['windSpeed']
            temp_color = get_temp_color(temperature)

            temperature_formatted = f"{temperature}F"
            max_temp_formatted = f"{max_temp}F"
            min_temp_formatted = f"{min_temp}F"
            wind_speed_formatted = f"{wind_speed}MPH"

            cleanDescription = get_clean_description(icon)
            desc_x = get_x_offset(icon)

            # Draw weather image
            weather_img = load_weather_image(icon)
            if weather_img:
                image.paste(weather_img, (0, 0))

            # Draw text
            draw_text(draw, temperature_formatted, (39, 6), temp_color, font)
            draw_text(draw, cleanDescription, (desc_x, -2), (255, 255, 255), font)
            draw_text(draw, wind_speed_formatted, (35, 14), (0, 255, 255), font)
            draw_text(draw, max_temp_formatted, (28, 22), (255, 0, 0), font)
            draw_text(draw, min_temp_formatted, (46, 22), (0, 0, 255), font)

            # Save fallback state
            global_temperature = temperature_formatted
            global_description = cleanDescription
            global_high_temp = max_temp_formatted
            global_low_temp = min_temp_formatted
            global_wind_speed = wind_speed_formatted
        else:
            # Draw fallback state or error
            draw_text(draw, "ERROR", (1, 15), (255, 0, 0), font)
            draw_text(draw, global_temperature, (39, 13), (0, 255, 0), font)
            draw_text(draw, global_description, (32, 3), (255, 255, 255), font)
            draw_text(draw, global_high_temp, (33, 27), (255, 0, 0), font)
            draw_text(draw, global_low_temp, (50, 27), (0, 0, 255), font)
            draw_text(draw, global_wind_speed, (35, 20), (0, 255, 255), font)

        # Display image on matrix
        matrix.SetImage(image)

        time.sleep(FETCH_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
