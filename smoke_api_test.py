import requests

# Base API URL
BASE_URL = "https://thinking-tester-contact-list.herokuapp.com"

# Test data
TEST_USER = {
    "firstName": "Dzenan",
    "lastName": "Kisic",
    "email": "dzenan@atlant.bh",
    "password": "SecurePassword123"
}

# API Endpoints
REGISTER_ENDPOINT = f"{BASE_URL}/users"
LOGIN_ENDPOINT = f"{BASE_URL}/users/login"
CONTACTS_ENDPOINT = f"{BASE_URL}/contacts"

# Log file path
LOG_FILE = "api_smoke_test_log.txt"

# Helper function for logging results
def log_result(message):
    print(message)
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")

# Smoke Test Suite
def run_api_smoke_tests():
    print("=== Automating API Smoke Testing ===")
    session_token = None
    try:
        # Step 1: User Registration
        print("[INFO] Testing user registration...")
        register_response = requests.post(REGISTER_ENDPOINT, json=TEST_USER)
        if register_response.status_code == 201:
            log_result("[PASS] User registration successful.")
        else:
            log_result("[FAIL] User registration failed.")
            return  # Stop further tests if registration fails

        # Step 2: User Login
        print("[INFO] Testing user login...")
        login_response = requests.post(LOGIN_ENDPOINT, json={
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        })
        if login_response.status_code == 200:
            session_token = login_response.json().get("token")
            log_result("[PASS] User login successful.")
        else:
            log_result("[FAIL] User login failed.")
            return  # Stop further tests if login fails

        headers = {"Authorization": f"Bearer {session_token}"}

        # Step 3: Add a Contact
        print("[INFO] Testing contact creation...")
        contact_data = {
            "firstName": "Sinan",
            "lastName": "Sakic",
            "email": "sinan.sakic@gmail.com",
            "phone": "123456789"
        }
        add_contact_response = requests.post(CONTACTS_ENDPOINT, json=contact_data, headers=headers)
        if add_contact_response.status_code == 201:
            contact_id = add_contact_response.json().get("_id")
            log_result("[PASS] Contact creation successful.")
        else:
            log_result("[FAIL] Contact creation failed.")
            return

        # Step 4: Get Contact List
        print("[INFO] Testing contact list retrieval...")
        get_contacts_response = requests.get(CONTACTS_ENDPOINT, headers=headers)
        if get_contacts_response.status_code == 200 and contact_data["email"] in str(get_contacts_response.json()):
            log_result("[PASS] Contact list retrieval successful.")
        else:
            log_result("[FAIL] Contact list retrieval failed.")

        # Step 5: Update the Contact
        print("[INFO] Testing contact update...")
        updated_contact_data = {
            "firstName": "Sinan",
            "lastName": "Sakic",
            "email": "sinan.updated@gmail.com",
            "phone": "987654321"
        }
        update_contact_response = requests.put(
            f"{CONTACTS_ENDPOINT}/{contact_id}", json=updated_contact_data, headers=headers
        )
        if update_contact_response.status_code == 200:
            log_result("[PASS] Contact update successful.")
        else:
            log_result("[FAIL] Contact update failed.")

        # Step 6: Delete the Contact
        print("[INFO] Testing contact deletion...")
        delete_contact_response = requests.delete(f"{CONTACTS_ENDPOINT}/{contact_id}", headers=headers)
        if delete_contact_response.status_code == 200:
            log_result("[PASS] Contact deletion successful.")
        else:
            log_result("[FAIL] Contact deletion failed.")

        # Step 7: Verify Contact Deletion
        print("[INFO] Verifying contact deletion...")
        verify_deletion_response = requests.get(CONTACTS_ENDPOINT, headers=headers)
        if verify_deletion_response.status_code == 200 and contact_data["email"] not in str(verify_deletion_response.json()):
            log_result("[PASS] Contact deletion verified.")
        else:
            log_result("[FAIL] Contact deletion verification failed.")

        print("[INFO] API Smoke Test Suite completed successfully.")

    except Exception as e:
        log_result(f"[ERROR] API Smoke Test Suite failed due to: {e}")

if __name__ == "__main__":
    run_api_smoke_tests()
