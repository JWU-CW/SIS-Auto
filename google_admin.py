from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
import sys

def create_google_account(first_name, last_name, email, temp_password):
    # Load environment variables from .env
    load_dotenv()
    username = os.getenv("GA_USER")
    password = os.getenv("GA_PW")

    if not username or not password:
        raise Exception("Missing Google Admin USER or PW in .env file")

    # Set up Chrome WebDriver
    chrome_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")  # Suppress Chrome logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress DevTools warnings
    options.add_argument("--no-first-run") # Disable "Sign in to Chrome" and other first-run popups
    options.add_argument("--no-default-browser-check")
    options.add_argument("--guest")

    driver = webdriver.Chrome(service=chrome_service, options=options)

    try:
        wait = WebDriverWait(driver, 10)

        # Step 1: Open login page
        driver.get("https://admin.google.com")

        username_input = wait.until(EC.element_to_be_clickable((By.ID, "identifierId")))
        username_input.send_keys(username)

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        next_button.click()

        password_input = wait.until(EC.element_to_be_clickable((By.NAME, "Passwd")))
        password_input.send_keys(password)

        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
        next_button.click()

        users_heading = wait.until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Users']"))
        )    
        driver.get("https://admin.google.com/ac/users?action_id=ADD_USER")
        
        first_name_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='First name *']"))
        )
        first_name_input.send_keys(first_name)

        last_name_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Last name *']"))
        )
        last_name_input.send_keys(last_name)

        primary_email_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Primary email *']"))
        )
        primary_email_input.send_keys(email)

        manage_span = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()=\"Manage user's password, organizational unit, and profile photo\"]"))
        )
        manage_span.click()

        radio_wrapper = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-label="Create password"]'))
        )
        radio_wrapper.click()

        password_input = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@aria-label='Enter password of 8 to 100 characters']"))
        )
        password_input.send_keys(temp_password)

        print("Please click the 'Add new user' button manually.")
        input("Press Enter here after you've clicked the button...")

        print("Account created. Closing browser.")

    finally:
        driver.quit()