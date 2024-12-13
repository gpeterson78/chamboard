from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
from waveshare_epd import epd7in5_V2  # Adjust for your specific display model

def capture_screenshot(url, screenshot_path="screenshot.png"):
    # Set up headless Firefox
    options = Options()
    options.add_argument("-headless")

    # Initialize the WebDriver
    driver = webdriver.Firefox(options=options)
    try:
        # Set the browser window size to 480x800
        driver.set_window_size(480, 800)

        # Load the URL
        driver.get(url)

        # Wait for the page to indicate it's fully loaded
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Optionally wait a bit longer for dynamic content to load (if needed)
        driver.implicitly_wait(3)

        # Capture the screenshot
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

    finally:
        # Ensure the browser is properly closed
        driver.quit()

def display_image(image_path):
    # Initialize the e-paper display
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()

    # Open the image and resize it to fit the display
    image = Image.open(image_path)
    image = image.resize((epd.height, epd.width), Image.ANTIALIAS).convert("1")  # Swap width and height
    image = image.rotate(90, expand=True)  # Rotate 90 degrees clockwise for portrait mode

    # Display the image on the e-paper
    epd.display(epd.getbuffer(image))

    # Put the e-paper display to sleep to save power
    epd.sleep()

if __name__ == "__main__":
    # URL to capture
    url = "https://www.gradyp.com/chamboard"  # Replace with your desired URL

    # Path to save the screenshot
    screenshot_path = "screenshot.png"

    # Step 1: Capture the screenshot
    capture_screenshot(url, screenshot_path)

    # Step 2: Display the screenshot on the e-paper
    display_image(screenshot_path)
