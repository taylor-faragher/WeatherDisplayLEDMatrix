WEATHER_CONFIG = {
    "01d": {
        "clean_description": "SUNNY",
        "description_color": 0xffffff,
        "image": "/images/sunny.bmp",
    },
    "02d": {
        "clean_description": "SUNNY",
        "description_color": 0xffffff,
        "image": "/images/sunny.bmp",
    },
    "03d": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "/images/cloudy.bmp",
    },
    "04d": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "/images/cloudy.bmp",
    },
    "09d": {
        "clean_description": "RAINY",
        "description_color": 0xffffff,
        "image": "/images/rain.bmp",
    },
    "10d": {
        "clean_description": "RAIN",
        "description_color": 0xffffff,
        "image": "/images/rain.bmp",
    },
    "11d": {
        "clean_description": "TSTORMS",
        "description_color": 0xffffff,
        "image": "/images/thunder.bmp",
    },
    "13d": {
        "clean_description": "SNOW",
        "description_color": 0xffffff,
        "image": "/images/snow.bmp",
    },
    "50d": {
        "clean_description": "MISTY",
        "description_color": 0xffffff,
        "image": "/images/cloudy.bmp",
    },
    "01n": {
        "clean_description": "CLEAR",
        "description_color": 0xffffff,
        "image": "/images/moon.bmp",
    },
    "02n": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "/images/cloudy.bmp",
    },
    "03n": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "/images/cloudy.bmp",
    },
    "04n": {
        "clean_description": "CLOUDY",
        "description_color": 0xffffff,
        "image": "/images/cloudy.bmp",
    },
    "09n": {
        "clean_description": "RAIN",
        "description_color": 0xffffff,
        "image": "/images/rain.bmp",
    },
    "10n": {
        "clean_description": "RAIN",
        "description_color": 0xffffff,
        "image": "/images/rain.bmp",
    },
    "11n": {
        "clean_description": "TSTORMS",
        "description_color": 0xffffff,
        "image": "/images/thunder.bmp",
    },
    "13n": {
        "clean_description": "SNOW",
        "description_color": 0xffffff,
        "image": "/images/snow.bmp",
    },
    "50n": {
        "clean_description": "MISTY",
        "description_color": 0xffffff,
        "image": "/images/cloudy.bmp",
    },
    "default": {
        "clean_description": "none",
        "description_color": 0xffffff,
        "image": "/images/cloudy.bmp",
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