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
from weather_config import get_clean_description, get_image_path

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
    x=39,
    y=13,
    scale=1,
)

description_area = Label(
    font,
    text="",
    color=0xffffff,
    x=32,
    y=3,
    scale=1,
)

wind_area = Label(
    font,
    text="",
    color=0x00FFFF,
    x=35,
    y=20,
    scale=1,
)

high_temp_area = Label(
    font,
    text="",
    color=0xFF0000,
    x=32,
    y=27,
    scale=1,
)

low_temp_area = Label(
    font,
    text="",
    color=0x0000FF,
    x=50,
    y=27,
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
group.append(wind_area)
group.append(high_temp_area)
group.append(low_temp_area)
group.append(error_area)

display.refresh()

def set_fetching_state():
    clear_error()
    status_area.text = "FETCHING..."
    temperature_area.text = ""
    description_area.text = ""
    wind_area.text = ""
    high_temp_area.text = ""
    low_temp_area.text = ""
    load_weather_image("none")

# --- Network setup ---
network = Network(status_neopixel=board.NEOPIXEL, debug=False)
network.connect()

def set_error():
    error_area.text = "."

def clear_error():
    error_area.text = ""

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
        image_key = get_image_path(condition)
        if condition is not "empty":
            bitmap = displayio.OnDiskBitmap(image_key)
            tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader, tile_width=32, tile_height=32, width=1, height=1)
            group.append(tile_grid)
            current_weather_tile_grid = tile_grid
        else:
            current_weather_tile_grid = None

while True:
    set_fetching_state()
    weather_data = fetch_weather_data(status_area, network_client=network)

    if weather_data:
        current = weather_data['current']

        # Access nested values
        temperature = current['temperature']
        icon = current['icon']
        temp_color = get_temp_color(temperature)
        temperature_area.color = temp_color

        # Format the temperature text
        text = f"{temperature}F"
        
        # Clean up the description
        cleanDescription = get_clean_description(icon)
        
        # Load the weather image
        load_weather_image(icon)
        
        # Update global variables
        GLOBAL_TEMPERATURE_VARIABLE = text
        GLOBAL_DESCRIPTION_VARIABLE = cleanDescription
        # Update text areas
        temperature_area.text = text
        description_area.text = cleanDescription
        high_temp_area.text = f"H {temperature}"
        low_temp_area.text = f"L {temperature}"
        wind_area.text = "10MPH"
    else:
        # Turn on error state
        set_error()
        # Set text to saved global variables
        temperature_area.text = GLOBAL_TEMPERATURE_VARIABLE
        description_area.text = GLOBAL_DESCRIPTION_VARIABLE
        load_weather_image(cleanDescription)
        print("Failed to fetch data")

    time.sleep(FETCH_INTERVAL_SECONDS)
