from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Configurations
webhook_url = os.getenv("DISCORD_WEBHOOK_URL", "<YOUR_DISCORD_WEBHOOK_URL>")
page_url = os.getenv("PAGE_URL", "https://store.steampowered.com/sale/steamdeckrefurbished/")

# Parse product titles from environment variable (comma-separated)
product_titles_env = os.getenv("PRODUCT_TITLES", "Steam Deck 512GB OLED - Valve Certified Refurbished,Steam Deck 1TB OLED - Valve Certified Refurbished")
product_titles = [title.strip() for title in product_titles_env.split(",") if title.strip()]

debug = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")

# Set up Selenium WebDriver options
options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service("/usr/bin/chromedriver")

# Start WebDriver
driver = webdriver.Chrome(service=service, options=options)
try:
    logging.info("Loading page...")
    driver.get(page_url)

    # Wait for page to load dynamic content
    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Extra wait to ensure all dynamic content is fully loaded
    time.sleep(3)

    # Set the window size to capture the full page
    driver.set_window_size(1920, 1500)
    
    product_found = False
    for title in product_titles:
        try:
            # Check if the product is available
            product_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{title}')]")
            
            # Locate the "Add to Cart" button (adjusted for your HTML structure)
            add_to_cart_button = product_element.find_element(By.XPATH, "..//following-sibling::*//*[contains(@class, 'CartBtn')]//span[contains(text(), 'Add to Cart')]")
            
            # Check if the "Add to Cart" button is present
            if add_to_cart_button.is_displayed():
                product_found = True
                logging.warning(f"STOCK FOUND: {title}")
                break
        except Exception as e:
            # If any exception occurs (e.g., product not found), continue checking other products
            continue

    # Take a full-page screenshot
    screenshot_path = "/tmp/steamdeck_stock_status.png"
    driver.save_screenshot(screenshot_path)

    # Send a notification if any of the products have an "Add to Cart" button visible
    if product_found or debug:
        logging.warning("Steam Deck is in stock! Sending notification")
            
        message = {
            "content": f"One of the Steam Deck models is now in stock! Check it out here: <{page_url}>",
        }
        files = {
            "file": ("screenshot.png", open(screenshot_path, "rb"))
        }
        response = requests.post(webhook_url, data=message, files=files)
        
        if response.status_code == 200:
            logging.info("Discord notification sent successfully")
        else:
            logging.error(f"Discord notification failed: {response.status_code}")
    else:
        logging.info("No Steam Deck models in stock")

finally:
    driver.quit()
    logging.info("Check completed")
