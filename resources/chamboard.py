from playwright.sync_api import sync_playwright
from PIL import Image
from waveshare_epd import epd7in5_V2  # Adjust for your specific display model

def capture_screenshot(url, screenshot_path="screenshot.png", width=480, height=800):
    with sync_playwright() as p:
        # Launch WebKit in headless mode
        browser = p.webkit.launch(headless=True)
        page = browser.new_page()

        # Set the viewport size
        page.set_viewport_size({"width": width, "height": height})

        # Navigate to the URL
        page.goto(url)

        # Wait for the page to fully load
        page.wait_for_load_state("networkidle")

        # Take the screenshot
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # Close the browser
        browser.close()

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
    # Define the URL to capture and the screenshot path
    url = "https://www.gradyp.com/chamboard"
    screenshot_path = "screenshot.png"

    # Step 1: Capture the screenshot
    capture_screenshot(url, screenshot_path)

    # Step 2: Display the screenshot on the e-paper
    display_image(screenshot_path)
