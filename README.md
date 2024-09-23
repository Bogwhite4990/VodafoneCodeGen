# Vodafone Voucher Code Checker

# Disclaimer

**<span style="color:red">This script is intended for testing and educational purposes only.  
It is your responsibility to ensure that any use of this script complies with the terms and conditions of the target website. Misuse of automation tools like this may lead to consequences such as being blocked from the website or legal issues.</span>**

Use this script at your own risk.

This Python script automatically generates random alphanumeric codes and checks their validity on the Vodafone Romania website by entering them into a cart page for a specific product. It uses Selenium to automate the web interaction and handles cookies, navigation, and voucher code input.

## Features
- Generates random voucher codes with a customizable prefix.
- Uses Selenium WebDriver to navigate the Vodafone Romania website and check codes.
- Saves checked codes to avoid repetition.
- Stores valid codes in a separate file.
- Runs in headless mode by default (without browser GUI).

## Prerequisites
To run this script, you'll need the following:

- **Python 3.x**
- **Selenium**: Install via pip:
  ```bash
  pip install selenium

  Geckodriver (for Firefox):

Download Geckodriver: Geckodriver releases.
Ensure it's available in your system's PATH or specify its path when creating the Service object in the script.
Mozilla Firefox Browser: Required for Selenium's Firefox WebDriver.

## How It Works
1. Generate Code: The script generates a random alphanumeric voucher code using the generate_code() function.
2. Navigate: It uses Selenium to open the Vodafone Romania cart page for a specific product.
3. Check Codes: The script enters each generated code into the voucher input field and submits the form.
4. Handle Errors: Based on the response (invalid or expired voucher), it either discards the code or saves valid ones.
5. Avoid Rechecking: Previously checked codes are stored in a text file to avoid repeating the same checks.

## Code Structure
generate_code(): Creates a random voucher code with a default prefix of "CB".
load_checked_codes(): Reads previously checked codes from a file to avoid repetition.
save_checked_code(): Saves checked codes (both valid and invalid) into a file.
setup_driver(): Initializes the Selenium WebDriver for Firefox in headless mode.
accept_cookies(): Automatically clicks on cookie consent buttons when navigating the website.
navigate_to_cart_page(): Navigates to the Vodafone Romania product page and selects necessary checkboxes.
check_code_on_cart_page(): Submits generated codes into the input field and processes the website’s response.
main(): The main loop that runs the entire process, generating and checking codes in an infinite loop until stopped.

## Output Files
checked_codes.txt: Stores all the checked codes (to prevent duplicates).
valid_codes.txt: Stores valid voucher codes found by the script.

## Notes
The script runs indefinitely until manually stopped.
You can modify the voucher code generation logic (length, prefix) based on your needs.
To visualize the browser while running, remove or comment out the firefox_options.add_argument("--headless") line in the setup_driver() function.

