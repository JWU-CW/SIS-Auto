from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time

# Ask for student ID
student_id = input("Enter Student ID: ")

# Setup WebDriver with ChromeDriverManager
chrome_service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")  # Only show fatal errors

# Create the driver properly
driver = webdriver.Chrome(service=chrome_service, options=options)

try:
    # Step 1: Go to the website
    url = "https://cwcs.plsis.com"
    driver.get(url)

   # Give the page some time to load
    time.sleep(1)

    # Step 2: Find the username and password fields by ID and type into them
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys("jwu")
    password_input.send_keys("Wzf104416!")

    # Step 3: Find the LOGIN button and click it
    login_button = driver.find_element(By.XPATH, "//button[normalize-space(text())='LOGIN'] | //input[@type='submit' and @value='LOGIN']")
    login_button.click()

    # Give the page some time to load
    time.sleep(1)

    # Step 4: Redirect to student list
    url = "https://cwcs.plsis.com/mod.php/admin/registration/studentlist.php"
    driver.get(url)

    # Step 5: Enter student id
    student_id_input = driver.find_element(By.ID, "entity-filter-search-name")
    student_id_input.send_keys(student_id)

    # Step 6: Find the Search button and click it
    login_button = driver.find_element(By.XPATH, "//button[normalize-space(text())='Search'] | //input[@type='submit' and @value='Search']")
    login_button.click()

    # Step 7: Find the link to the student profile and click it
    wait = WebDriverWait(driver, 5)
    first_link = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#sp_datatable_entity_list_table tbody tr a")
    ))
    first_link.click()

    # Let the user see the result for 3 seconds before closing
    print("Search submitted. The browser will close in 3 seconds...")
    time.sleep(5)

finally:
    driver.quit()
