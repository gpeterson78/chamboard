import logging
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright
from PIL import Image
from waveshare_epd import epd7in5_V2  # Adjust for your specific display model

# Configure logging
LOG_DIR = Path.home() / "chamboard" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "chamboard.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def log_and_print(message, level="info"):
    """Helper function to log and print messages."""
    if level == "info":
        logging.info(message)
    elif level == "error":
        logging.error(message)
    elif level == "warning":
        logging.warning(message)
    print(message)

def capture_screenshot(url, screenshot_path="screenshot.png", width=480, height=800):
    try:
        with sync_playwright() as p:
            browser = p.webkit.launch(headless=True)
            page = browser.new_page()
            page.set_viewport_size({"width": width, "height": height})
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=screenshot_path)
            log_and_print(f"Screenshot saved to {screenshot_path}")
            browser.close()
    except Exception as e:
        log_and_print(f"Error capturing screenshot: {e}", level="error")

def display_image(image_path):
    try:
        epd = epd7in5_V2.EPD()
        epd.init()
        epd.Clear()
        image = Image.open(image_path)
        image = image.resize((epd.height, epd.width), Image.Resampling.LANCZOS).convert("1")
        image = image.rotate(90, expand=True)
        epd.display(epd.getbuffer(image))
        epd.sleep()
        log_and_print("Image displayed successfully on e-paper.")
    except Exception as e:
        log_and_print(f"Error displaying image: {e}", level="error")

if __name__ == "__main__":
    url = "https://www.gradyp.com/chamboard"
    screenshot_path = "screenshot.png"
    log_and_print("Starting chamboard script.")
    capture_screenshot(url, screenshot_path)
    display_image(screenshot_path)
    log_and_print("Chamboard script completed successfully.")
