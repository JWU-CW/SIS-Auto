from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from helper import split_name, generate_random_string, generate_OU_path, add_user_to_csv
from dotenv import load_dotenv
import os
import time
import sys
import csv

# Define the CSV file path
csv_file = 'data.csv'

def search_student_by_id():
    # Load environment variables from .env
    load_dotenv()
    username = os.getenv("SIS_USER")
    password = os.getenv("SIS_PW")

    if not username or not password:
        raise Exception("Missing SIS USER or PW in .env file")

    # Ask for student ID
    student_id = input("Enter Student ID: ")

    # Set up Chrome WebDriver
    chrome_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")  # Suppress Chrome logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress DevTools warnings

    driver = webdriver.Chrome(service=chrome_service, options=options)

    try:
        wait = WebDriverWait(driver, 10)

        # Step 1: Open login page
        driver.get("https://cwcs.plsis.com")

        # Step 2: Log in with credentials
        username_input = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username_input.send_keys(username)

        password_input = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password_input.send_keys(password)

        login_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space(text())='LOGIN'] | //input[@type='submit' and @value='LOGIN']")
        ))
        login_button.click()

        # Step 3: Go to student list page
        student_search_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Find/Add Student")))
        student_search_url = student_search_link.get_attribute("href")
        driver.get(student_search_url)

        # Step 4: Enter student ID and search
        student_id_input = wait.until(EC.element_to_be_clickable((By.ID, "entity-filter-search-name")))
        student_id_input.send_keys(student_id)
        
        search_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space(text())='Search'] | //input[@type='submit' and @value='Search']")
        ))
        search_button.click()

        # Step 5: Click on the first student result
        try:
            first_link = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#sp_datatable_entity_list_table tbody tr a")
            ))
            first_link.click()
        except TimeoutException:
            print("❌ Student not found")
            sys.exit()

        # Step 6: Extract info from student profile page
        name = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "h2.student-profile-name")
        )).text

        grade = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//td[./b[text()='Grade:']]/following-sibling::td")
        )).text

        district_id = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//td[./b[text()='District:']]/following-sibling::td")
        )).text

        email = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//li[b[text()='Email']]/following-sibling::li[1]/a")
        )).text

        try:
            ES_link = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "#sp-panel-staff table.sp-panel-table tbody tr a")
            ))
            ES_url = ES_link.get_attribute("href")
            driver.get(ES_url)
        except TimeoutException:
            print("❌ Could not find the student's ES")
            sys.exit()
        
        # Step 6: Extract info from staff profile page
        ES_name = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "h2.staff-profile-name ")
        )).text
        ES_email = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//li[b[text()='Work Email:']]/a")
        )).text

        print("--------------------------------------------------")
        print("Student Name: " + name)
        print("Grade: " + grade)
        print("District ID: " + district_id)
        print("Contact Email: " + email)
        print("ES Name: " + ES_name)
        print("ES Email: " + ES_email)
        print("--------------------------------------------------")
        
        # Step 7: Return the results
        print("Search submitted.")
        
        res = split_name(name)
        res["email"] = district_id
        res["password"] = generate_random_string()
        
        ES = split_name(ES_name)
        row = [
            res['first_name'],
            res['last_name'],
            district_id + "@cwcharter.org",
            res['password'],
            generate_OU_path(grade),
            ES['first_name'],
            ES['last_name'],
            ES_email
        ]
        add_user_to_csv(row)

        return res

    except Exception as e:
        print("❌ Error fetching student's info")
        print(e)

    finally:
        driver.quit()
