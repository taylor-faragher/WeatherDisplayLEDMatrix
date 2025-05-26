from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# --- Display setup ---
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'

matrix = RGBMatrix(options=options)
largeFont = graphics.Font()
largeFont.LoadFont("fonts/TaylorsLEDFont-8pt.bdf")

def main():
    while True:
        # Clear the display
        matrix.Clear()

        # Draw some text using the large font
        graphics.DrawText(matrix, largeFont, 1, 1, graphics.Color(255, 255, 255), "ABCDEFGHIJK")
        
        # Optionally, you can draw more text or graphics here
        graphics.DrawText(matrix, largeFont, 1, 10, graphics.Color(0, 255, 0), "LMNOPQRSTU")
        graphics.DrawText(matrix, largeFont, 1, 20, graphics.Color(0, 0, 255), "VWXYZ")


if __name__ == "__main__":
    main()