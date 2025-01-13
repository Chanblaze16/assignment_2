import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert


def read_data_from_file(file_path):
    input_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                input_data[key.strip()] = value.strip()
    return input_data


def read_locators_from_file(file_path):
    locators = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                locators[key.strip()] = value.strip()
    return locators

def read_credentials_from_file(file_path):
    credentials = {}
    with open(file_path, 'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                credentials[key.strip()] = value.strip()
    return credentials

def login_to_salesforce(driver, username, password):
    driver.get("https://login.salesforce.com")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "Login").click()

def create_lead(driver, locators, input_data):
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, locators['lead_name_xpath']))
    )
    driver.find_element(By.XPATH, locators['lead_name_xpath']).click()
    time.sleep(2)
    driver.find_element(By.XPATH, locators['lead_first_name_xpath']).send_keys(input_data['lead_first_name'])
    time.sleep(2)
    driver.find_element(By.XPATH, locators['lead_last_name_xpath']).send_keys(input_data['lead_last_name'])
    time.sleep(1)
    driver.find_element(By.XPATH, locators['lead_company_xpath']).send_keys(input_data['lead_company'])
    driver.find_element(By.XPATH, locators['lead_save_button_xpath']).click()
    time.sleep(1)

def create_account(driver, locators, input_data):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, locators['convert_button_xpath']))
    )
    driver.find_element(By.XPATH, locators['convert_button_xpath']).click()
    time.sleep(2)
    driver.find_element(By.XPATH, locators['convert2_button_xpath']).click()
    time.sleep(3)

def attach_contact_to_account(driver, locators, input_data):
    driver.find_element(By.XPATH, locators['select_account']).click()
    time.sleep(1)
    driver.find_element(By.XPATH, locators['new_contact_button']).click()
    time.sleep(1)
    driver.find_element(By.XPATH, locators['contact_lastname_xpath']).send_keys(input_data['contact_last_name'].split(" ")[0])
    time.sleep(1)
    driver.find_element(By.XPATH, locators['contact_save_button']).click()
    time.sleep(1)

def create_opportunity(driver, locators, opportunity_data):
    # Create opportunity linked to the account
    driver.find_element(By.XPATH, locators['opportunity_button_xpath']).click()
    time.sleep(1)
    driver.find_element(By.XPATH, locators['opportunity_save_button']).click()
    time.sleep(3)

def main_use_case_1_and_2():
    driver = webdriver.Chrome()
    driver.maximize_window()
    locators = read_locators_from_file("locators.txt")
    input_data = read_data_from_file("input_data.txt")  # This would contain data like lead_name, lead_phone, etc.
    credentials = read_credentials_from_file("credentials.txt")

    username = credentials.get("username")
    password = credentials.get("password")

    login_to_salesforce(driver, username, password)
    create_lead(driver, locators, input_data)
    create_account(driver, locators, input_data)
    attach_contact_to_account(driver, locators, input_data)
    create_opportunity(driver, locators, input_data)

    driver.quit()


if __name__ == "__main__":
    main_use_case_1_and_2()
