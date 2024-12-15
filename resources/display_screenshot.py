from PIL import Image
from waveshare_epd import epd7in5_V2  # Adjust for your specific display model

def display_image(image_path):
    # Initialize the e-paper display
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    # Open the image and resize it to fit the display
    image = Image.open(image_path)
    image = image.resize((epd.height, epd.width), Image.Resampling.LANCZOS).convert("1")  # Swap width and height
    image = image.rotate(90, expand=True)  # Rotate 90 degrees clockwise for portrait mode

    # Display the image on the e-paper
    epd.display(epd.getbuffer(image))
    
    # Put the e-paper display to sleep to save power
    epd.sleep()

if __name__ == "__main__":
    # Path to the screenshot
    screenshot_path = "screenshot.png"  # Update this to your actual path

    # Display the screenshot on the e-paper
    display_image(screenshot_path)