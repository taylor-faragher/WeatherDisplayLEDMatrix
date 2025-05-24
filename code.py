import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
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

# Load a BDF font (use your own or one from the rpi-rgb-led-matrix/fonts directory)
font = graphics.Font()
font.LoadFont("fonts/TaylorsLEDFont-5.bdf")  # Change to your font path if needed

def int_to_rgb(color_int):
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    return (r, g, b)

def load_weather_image(condition):
    if condition == "none":
        return None
    image_path = get_image_path(condition)
    try:
        # rpi-rgb-led-matrix can load PPM, PGM, and some BMPs directly
        # We'll use graphics.DrawLine to draw a simple icon, or you can use the sample image-viewer.py for more complex images
        # For now, let's skip image loading for simplicity
        return None
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def draw_text(matrix, font, text, x, y, color):
    graphics.DrawText(matrix, font, x, y, color, text)

def main():
    global_temperature = ""
    global_description = ""
    global_high_temp = ""
    global_low_temp = ""
    global_wind_speed = ""

    while True:
        # Clear the display
        matrix.Clear()

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
            r, g, b = int_to_rgb(temp_color)
            draw_text(matrix, font, temperature_formatted, 39, 13, graphics.Color(r, g, b))

            temperature_formatted = f"{temperature}F"
            max_temp_formatted = f"{max_temp}F"
            min_temp_formatted = f"{min_temp}F"
            wind_speed_formatted = f"{wind_speed}MPH"

            cleanDescription = get_clean_description(icon)
            desc_x = get_x_offset(icon)

            # Draw weather image (optional, see note above)
            # If you want to display an image, use the rgbmatrix sample image-viewer.py as a reference

            # Draw text
            draw_text(matrix, font, temperature_formatted, 39, 13, graphics.Color(*temp_color))
            draw_text(matrix, font, cleanDescription, desc_x, 3, graphics.Color(255, 255, 255))
            draw_text(matrix, font, wind_speed_formatted, 35, 20, graphics.Color(0, 255, 255))
            draw_text(matrix, font, max_temp_formatted, 33, 27, graphics.Color(255, 0, 0))
            draw_text(matrix, font, min_temp_formatted, 50, 27, graphics.Color(0, 0, 255))

            # Save fallback state
            global_temperature = temperature_formatted
            global_description = cleanDescription
            global_high_temp = max_temp_formatted
            global_low_temp = min_temp_formatted
            global_wind_speed = wind_speed_formatted
        else:
            # Draw fallback state or error
            draw_text(matrix, font, "ERROR", 1, 15, graphics.Color(255, 0, 0))
            draw_text(matrix, font, global_temperature, 39, 13, graphics.Color(0, 255, 0))
            draw_text(matrix, font, global_description, 32, 3, graphics.Color(255, 255, 255))
            draw_text(matrix, font, global_high_temp, 33, 27, graphics.Color(255, 0, 0))
            draw_text(matrix, font, global_low_temp, 50, 27, graphics.Color(0, 0, 255))
            draw_text(matrix, font, global_wind_speed, 35, 20, graphics.Color(0, 255, 255))

        time.sleep(FETCH_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
