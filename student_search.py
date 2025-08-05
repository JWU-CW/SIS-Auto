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

def search_student_by_id():
    # Load environment variables from .env
    load_dotenv()
    username = os.getenv("SIS_USER")
    password = os.getenv("SIS_PW")

    if not username or not password:
        raise Exception("Missing USER or PW in .env file")

    # Ask for student ID
    student_id = input("Enter Student ID: ")

    # Set up Chrome WebDriver
    chrome_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")  # Suppress Chrome logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress DevTools warnings

    driver = webdriver.Chrome(service=chrome_service, options=options)

    try:
        # Step 1: Open login page
        driver.get("https://cwcs.plsis.com")
        time.sleep(1)

        # Step 2: Log in with credentials
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        login_button = driver.find_element(
            By.XPATH, "//button[normalize-space(text())='LOGIN'] | //input[@type='submit' and @value='LOGIN']"
        )
        login_button.click()
        time.sleep(1)

        # Step 3: Go to student list page
        driver.get("https://cwcs.plsis.com/mod.php/admin/registration/studentlist.php")

        # Step 4: Enter student ID and search
        student_id_input = driver.find_element(By.ID, "entity-filter-search-name")
        student_id_input.send_keys(student_id)
        search_button = driver.find_element(
            By.XPATH, "//button[normalize-space(text())='Search'] | //input[@type='submit' and @value='Search']"
        )
        search_button.click()

        # Step 5: Click on the first student result
        wait = WebDriverWait(driver, 5)
        try:
            first_link = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#sp_datatable_entity_list_table tbody tr a")
            ))
            first_link.click()
        except TimeoutException:
            print("❌ Student not found")
            sys.exit()

        # Step 6: Extract info from student profile page
        name = driver.find_element(By.CSS_SELECTOR, "h2.student-profile-name").text
        
        district_id = driver.find_element(
            By.XPATH, "//td[./b[text()='District:']]/following-sibling::td"
        ).text

        email = driver.find_element(
            By.XPATH, "//li[b[text()='Email']]/following-sibling::li[1]/a"
        ).text

        print("--------------------------------------------------")
        print("Student Name: " + name)
        print("District ID: " + district_id)
        print("Contact Email: " + email)
        print("--------------------------------------------------")
        # Step 6: Hold the result briefly
        print("Search submitted. The browser will close in 3 seconds...")
        time.sleep(3)

    finally:
        driver.quit()
