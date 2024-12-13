from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait

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


if __name__ == "__main__":
    # URL to capture
    url = "https://www.gradyp.com/chamboard"  # Replace with the desired URL

    # Path to save the screenshot
    screenshot_path = "screenshot.png"

    # Capture the screenshot
    capture_screenshot(url, screenshot_path)