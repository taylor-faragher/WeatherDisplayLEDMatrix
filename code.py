import time
import displayio
import terminalio
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text.label import Label
from adafruit_matrixportal.network import Network
from adafruit_bitmap_font import bitmap_font
import board
from weather_api import fetch_weather_data

FETCH_INTERVAL_SECONDS = 900 # 15 minutes

# --- Display setup ---
matrix = Matrix(width=64, height=32, bit_depth=4)
display = matrix.display

current_weather_tile_grid = None

WEATHER_IMAGES = {
        "Sunny": "/images/sunny.bmp",
        "Clear": "/images/moon.bmp",
        "Cldy": "/images/cloudy.bmp",
        "Rain": "/images/rain.bmp",
        "TStorms": "/images/thunder.bmp",
        "Snow": "/images/snow.bmp",
        "Misty": "/images/cloudy.bmp",
    }

# Create a display group
group = displayio.Group()
display.root_group = group

image_grid = None
image_index = 0 

font = bitmap_font.load_font("fonts/Roboto-Regular-8pt.bdf")

# Add labels for showing the data
status_area = Label(
    terminalio.FONT,
    text="Loading...",
    color=0x00FF00,
    x=1,
    y=15,
    scale=1,
)

temperature_area = Label(
    terminalio.FONT,
    text="",
    color=0x00FF00,
    x=40,
    y=24,
    scale=1,
)

description_area = Label(
    terminalio.FONT,
    text="",
    color=0xffffff,
    x=33,
    y=8,
    scale=1,
)

error_area = Label(
    terminalio.FONT,
    text="",
    color=0xFF0000,
    x=61,
    y=28,
    scale=1,
)

# Add ALL labels to the group immediately
group.append(status_area)
group.append(temperature_area)
group.append(description_area)
group.append(error_area)

display.refresh()

# --- Network setup ---
network = Network(status_neopixel=board.NEOPIXEL, debug=False)
network.connect()

def set_error():
    error_area.text = "."

def clear_error():
    error_area.text = ""

def clean_condition(condition, is_day):
    condition_mapping = {
        "01d":"Sunny",
        "02d":"Clear",
        "03d":"Cldy",
        "04d":"Cldy",
        "09d":"Rain",
        "10d":"Rain",
        "11d":"TStorms",
        "13d":"Snow",
        "50d":"Misty",
        "01n":"Clear",
        "02n":"Cldy",
        "03n":"Cldy",
        "04n":"Cldy",
        "09n":"Rain",
        "10n":"Rain",
        "11n":"TStorms",
        "13n":"Snow",
        "50n":"Misty",
    }
    return condition_mapping.get(condition, condition)

def load_weather_image(condition):
    """Load the appropriate weather image based on the condition."""
    global current_weather_tile_grid
    if current_weather_tile_grid is not None:
        try:
            if current_weather_tile_grid in group:
                group.remove(current_weather_tile_grid)
        except ValueError:
            pass
    if condition is None:
        return

    image_key = WEATHER_IMAGES.get(condition, "/images/sunny.bmp")
    if condition is not "empty":
        bitmap = displayio.OnDiskBitmap(image_key)
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, tile_width=32, tile_height=32, width=1, height=1)
        group.append(tile_grid)
        current_weather_tile_grid = tile_grid

while True:
    clear_error()
    weather_data = fetch_weather_data(status_area, network_client=network)

    if weather_data:
        current = weather_data['current']

        # Access nested values
        temperature = current['temperature']
        icon = current['icon']

        # Format the temperature text
        text = "{}°F".format(temperature)
        
        # Clean up the description
        cleanDescription = clean_condition(icon, True)
        
        # Load the weather image
        load_weather_image(cleanDescription)
        
        # Update text areas
        temperature_area.text = text
        description_area.text = cleanDescription
    else:
        set_error()
        print("Failed to fetch data")

    time.sleep(FETCH_INTERVAL_SECONDS)
