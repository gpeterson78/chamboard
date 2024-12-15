from playwright.sync_api import sync_playwright

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

# Example usage
if __name__ == "__main__":
    # Replace the URL with the target website
    capture_screenshot("https://www.gradyp.com/chamboard", "screenshot.png")
