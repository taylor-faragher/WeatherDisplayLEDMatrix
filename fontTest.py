from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time

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

def draw_text(matrix, font, text, x, y, color):
    graphics.DrawText(matrix, font, x, y, color, text)

def main():
    while True:
        # Clear the display
        matrix.Clear()

        # Draw some text using the large font
        draw_text(matrix, largeFont, "ABCDEFGHIJ", 1, 6, graphics.Color(255, 255, 255))
        
        # Optionally, you can draw more text or graphics here
        draw_text(matrix, largeFont, "KLMNOPQRST", 1, 16, graphics.Color(255, 255, 255))
        draw_text(matrix, largeFont, "UVWXYZ", 1, 26, graphics.Color(255, 255, 255))

        time.sleep(900)

if __name__ == "__main__":
    main()