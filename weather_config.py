WEATHER_CONFIG = {
    "01d": {
        "clean_description": "SUNNY",
        "description_color": 0xffffff,
        "image": "images/sunny.bmp",
        "x_offset": 34,
    },
    "02d": {
        "clean_description": "SUNNY",
        "description_color": 0xffffff,
        "image": "images/sunny.bmp",
        "x_offset": 34,
    },
    "03d": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "images/cloudy.bmp",
        "x_offset": 34,
    },
    "04d": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "images/cloudy.bmp",
        "x_offset": 34,
    },
    "09d": {
        "clean_description": "RAIN",
        "description_color": 0xffffff,
        "image": "images/rain.bmp",
        "x_offset": 38,
    },
    "10d": {
        "clean_description": "RAIN",
        "description_color": 0xffffff,
        "image": "images/rain.bmp",
        "x_offset": 38,
    },
    "11d": {
        "clean_description": "TSTORMS",
        "description_color": 0xffffff,
        "image": "images/thunder.bmp",
        "x_offset": 32,
    },
    "13d": {
        "clean_description": "SNOW",
        "description_color": 0xffffff,
        "image": "images/snowy.bmp",
        "x_offset": 37,
    },
    "50d": {
        "clean_description": "MISTY",
        "description_color": 0xffffff,
        "image": "images/cloudy.bmp",
        "x_offset": 35,
    },
    "01n": {
        "clean_description": "CLEAR",
        "description_color": 0xffffff,
        "image": "images/moon.bmp",
        "x_offset": 37,
    },
    "02n": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "images/cloudy.bmp",
        "x_offset": 34,
    },
    "03n": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "images/cloudy.bmp",
        "x_offset": 34,
    },
    "04n": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "images/cloudy.bmp",
        "x_offset": 34,
    },
    "09n": {
        "clean_description": "RAIN",
        "description_color": 0xffffff,
        "image": "images/rain.bmp",
        "x_offset": 38,
    },
    "10n": {
        "clean_description": "RAIN",
        "description_color": 0xffffff,
        "image": "images/rain.bmp",
        "x_offset": 38,
    },
    "11n": {
        "clean_description": "TSTORMS",
        "description_color": 0xffffff,
        "image": "images/thunder.bmp",
        "x_offset": 32,
    },
    "13n": {
        "clean_description": "SNOW",
        "description_color": 0xffffff,
        "image": "images/snowy.bmp",
        "x_offset": 37,
    },
    "50n": {
        "clean_description": "MISTY",
        "description_color": 0xffffff,
        "image": "images/cloudy.bmp",
        "x_offset": 35,
    },
    "default": {
        "clean_description": "none",
        "description_color": 0xffffff,
        "image": "images/cloudy.bmp",
        "x_offset": 32,
    },
}

def get_weather_config(condition_code):
    return WEATHER_CONFIG.get(condition_code, WEATHER_CONFIG["default"])

def get_clean_description(condition_code):
    config = get_weather_config(condition_code)
    return config["clean_description"]

def get_description_color(condition_code):
    config = get_weather_config(condition_code)
    return config["description_color"]

def get_image_path(condition_code):
    config = get_weather_config(condition_code)
    return config["image"]

def get_x_offset(condition_code):
    config = get_weather_config(condition_code)
    return config["x_offset"]