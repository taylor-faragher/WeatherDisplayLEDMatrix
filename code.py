import time
import displayio
import terminalio
from adafruit_matrixportal.matrix import Matrix
from adafruit_display_text.label import Label
from adafruit_matrixportal.network import Network
from adafruit_bitmap_font import bitmap_font
import board
from weather_api import fetch_weather_data
from get_temp_color import get_temp_color

FETCH_INTERVAL_SECONDS = 900 # 15 minutes
GLOBAL_TEMPERATURE_VARIABLE = 0
GLOBAL_DESCRIPTION_VARIABLE = ""

# --- Display setup ---
matrix = Matrix(width=64, height=32, bit_depth=4)
display = matrix.display

current_weather_tile_grid = None

# Create a display group
group = displayio.Group()
display.root_group = group

image_grid = None
image_index = 0 

font = bitmap_font.load_font("fonts/TaylorsLEDFont-5.bdf")

# Add labels for showing the data
status_area = Label(
    terminalio.FONT,
    text="LOADING...",
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
    font,
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

def clean_condition(condition):
    condition_mapping = {
        "01d":"SUNNY",
        "02d":"SUNNY",
        "03d":"CLOUDY",
        "04d":"CLOUDY",
        "09d":"RAINY",  
        "10d":"RAIN",
        "11d":"TSTORMS",
        "13d":"SNOW",
        "50d":"MISTY",
        "01n":"CLEAR",
        "02n":"CLOUDY",
        "03n":"CLOUDY",
        "04n":"CLOUDY",
        "09n":"RAIN",
        "10n":"RAIN",
        "11n":"TSTORMS",
        "13n":"SNOW",
        "50n":"MISTY",
    }
    return condition_mapping.get(condition, condition)

WEATHER_IMAGES = {
        "SUNNY": "/images/sunny.bmp",
        "CLEAR": "/images/moon.bmp",
        "CLOUDY": "/images/cloudy.bmp",
        "RAIN": "/images/rain.bmp",
        "TSTORMS": "/images/thunder.bmp",
        "SNOW": "/images/snow.bmp",
        "MISTY": "/images/cloudy.bmp",
    }

def load_weather_image(condition):
    """Load the appropriate weather image based on the condition."""
    global current_weather_tile_grid
    if current_weather_tile_grid is not None:
        try:
            if current_weather_tile_grid in group:
                group.remove(current_weather_tile_grid)
        except ValueError:
            pass
    if condition == "none":
        current_weather_tile_grid = None
        return

    if condition is not None:
        image_key = WEATHER_IMAGES.get(condition, "/images/sunny.bmp")
        if condition is not "empty":
            bitmap = displayio.OnDiskBitmap(image_key)
            tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, tile_width=32, tile_height=32, width=1, height=1)
            group.append(tile_grid)
            current_weather_tile_grid = tile_grid
        else:
            current_weather_tile_grid = None

def set_loading_state():
    clear_error()
    status_area.text = "LOADING..."
    temperature_area.text = ""
    description_area.text = ""
    load_weather_image("none")

while True:
    set_loading_state()
    weather_data = fetch_weather_data(status_area, network_client=network)

    if weather_data:
        current = weather_data['current']

        # Access nested values
        temperature = current['temperature']
        icon = current['icon']
        temp_color = get_temp_color(temperature)
        temperature_area.color = temp_color
        # Format the temperature text
        text = "{}°F".format(temperature)
        
        # Clean up the description
        cleanDescription = clean_condition(icon)
        
        # Load the weather image
        load_weather_image(cleanDescription)
        
        # Update global variables
        GLOBAL_TEMPERATURE_VARIABLE = text
        GLOBAL_DESCRIPTION_VARIABLE = cleanDescription
        # Update text areas
        temperature_area.text = text
        description_area.text = cleanDescription
    else:
        # Turn on error state
        set_error()
        # Set text to saved global variables
        temperature_area.text = GLOBAL_TEMPERATURE_VARIABLE
        description_area.text = GLOBAL_DESCRIPTION_VARIABLE
        load_weather_image(cleanDescription)
        print("Failed to fetch data")

    time.sleep(FETCH_INTERVAL_SECONDS)
