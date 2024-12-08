from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Constants
BASE_URL = "https://thinking-tester-contact-list.herokuapp.com"
NEW_USER = {
    "firstname":"Dzenan",
    "lastname":"Kisic",
    "email": "dzenan1@atlant.bh",
    "password": "securepassword123"
    }

CHROME_DRIVER_PATH = "C:/webdrivers/chromedriver.exe"

def log_result(message):
    """Logs test results to a file."""
    with open("ui_smoke_test_log.txt", "a") as file:
        file.write(message + "\n")

def run_ui_tests():
    print("=== Automated UI Smoke Testing ===")
    try:
        # Setup ChromeDriver
        chrome_options = Options()
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = Service(CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()

        # Step 1: Navigate to the login page
        driver.get(BASE_URL)
        log_result("[INFO] Navigated to the application URL.")

        # Wait for the 'email' field to be visible
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )

        # Step 2: Try logging in with incorrect credentials
        print("[INFO] Testing login with incorrect credentials...")
        driver.find_element(By.ID, "email").send_keys("wronguser@example.com")
        driver.find_element(By.ID, "password").send_keys("wrongpassword")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        if "Contact List" in driver.page_source:
            print("[PASS] Login with incorrect credentials failed as expected.")
            log_result("[PASS] Login with incorrect credentials failed as expected.")

        else:
            print("[FAIL] Login with incorrect credentials did not fail as expected.")
            log_result("[FAIL] Login with incorrect credentials did not fail as expected.")

        # Step 3: Try logging in with empty fields
        print("[INFO] Testing login with empty fields...")
        driver.find_element(By.ID, "email").clear()
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        if "Contact List" in driver.page_source:
            print("[PASS] Login with empty fields failed as expected.")
            log_result("[PASS] Login with empty fields failed as expected.")

        else:
            print("[FAIL] Login with empty fields did not fail as expected.")
            log_result("[FAIL] Login with empty fields did not fail as expected.")

        # Step 4: Register a new user
        print("[INFO] Proceeding to user registration...")
        driver.find_element(By.ID, "signup").click()
        time.sleep(2)

        # Wait for the registration fields to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "firstName"))
        )

        # Find and fill out the registration fields
        driver.find_element(By.ID, "firstName").send_keys(NEW_USER["firstname"])
        driver.find_element(By.ID, "lastName").send_keys(NEW_USER["lastname"])
        driver.find_element(By.ID, "email").send_keys(NEW_USER["email"])
        driver.find_element(By.ID, "password").send_keys(NEW_USER["password"])
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        
        if "Contact List" in driver.page_source:
            log_result("[PASS] User registration successful.")
            print("[PASS] User registration successful.")
        else:
            log_result("[FAIL] User registration failed.")
            print("[FAIL] User registration failed.")


        # Step 5: Add a new contact
        print("[INFO] Adding a new contact...")
        driver.find_element(By.ID, "add-contact").click()
        time.sleep(1)
        driver.find_element(By.ID, "firstName").send_keys("Saban")
        driver.find_element(By.ID, "lastName").send_keys("Saulic")
        driver.find_element(By.ID, "email").send_keys("saban.saulic@gmail.com")
        driver.find_element(By.ID, "phone").send_keys("123456789")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        if "John Doe" in driver.page_source:
            log_result("[PASS] Contact successfully added.")
            print("[PASS] Contact successfully added.")
        else:
            log_result("[FAIL] Failed to add a new contact.")
            print("[FAIL] Failed to add a new contact.")

        # Step 6: Edit the contact
        print("[INFO] Editing the contact...")
        driver.find_element(By.XPATH, "//tr[td[contains(text(), 'Saban Saulic')]]//td[contains(text(), 'Saban Saulic')]").click()
        time.sleep(1)

        driver.find_element(By.ID, "edit-contact").click()
        time.sleep(1)


        driver.find_element(By.ID, "phone").clear()
        driver.find_element(By.ID, "phone").send_keys("987654321")
        driver.find_element(By.ID, "submit").click()
        time.sleep(2)
        if "987654321" in driver.page_source:
            log_result("[PASS] Contact successfully edited.")
            print("[PASS] Contact successfully edited.")
        else:
            log_result("[FAIL] Failed to edit the contact.")
            print("[FAIL] Failed to edit the contact.")

        # Step 7: Delete the contact
        print("[INFO] Deleting the contact...")

        driver.find_element(By.ID, "delete").click()
        time.sleep(2)
    
        alert = Alert(driver)

        alert.accept()

        if "John Doe" not in driver.page_source:
            log_result("[PASS] Contact successfully deleted.")
            print("[PASS] Contact successfully deleted.")
        else:
            log_result("[FAIL] Failed to delete the contact.")
            print("[FAIL] Failed to delete the contact.")

        # Step 8: Logout
        print("[INFO] Logging out...")
        time.sleep(1)
        driver.find_element(By.ID, "logout").click()
        time.sleep(2)
        if "Log In" in driver.page_source:
            log_result("[PASS] Logout successful.")
            print("[PASS] Logout successful.")
        else:
            log_result("[FAIL] Logout failed.")
            print("[FAIL] Logout failed.")

        driver.quit()
        print("[INFO] UI Test Suite completed successfully.")
        log_result("[INFO] UI Test Suite completed successfully.")

    except Exception as e:
        print(f"[ERROR] UI Test Suite failed due to: {e}")
        log_result(f"[ERROR] UI Test Suite failed due to: {e}")

if __name__ == "__main__":
    run_ui_tests()
