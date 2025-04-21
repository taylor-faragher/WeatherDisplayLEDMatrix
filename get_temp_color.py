def get_temp_color(temp_fahrenheit):
    """
    Returns a color tuple (R, G, B) based on the temperature in Fahrenheit.
    Colder temperatures will be bluer, warmer will be redder.
    """
    if temp_fahrenheit <= 50:
        #Blue
        return 0x0000FF
    elif temp_fahrenheit >= 85:
        #Red
        return 0xFF0000
    else:
        # Interpolate between blue and red
        # Normalize temperature to a 0-1 range within the 50-85°F range
        normalized_temp = (temp_fahrenheit - 50) / (85 - 50)
        red = int(255 * normalized_temp)
        blue = int(255 * (1 - normalized_temp))
        return (red << 16) + blue