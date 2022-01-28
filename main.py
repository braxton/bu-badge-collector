import datetime
import sys
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pyicloud import PyiCloudService
from dotenv import load_dotenv


def init_driver():
    chrome_service = Service(os.getenv("CHROMEDRIVER_PATH"))
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.set_window_size(width=os.getenv("WINDOW_WIDTH"), height=os.getenv("WINDOW_HEIGHT"))

    return driver


def login(driver):
    driver.get("https://patientconnect.bu.edu")
    assert "Boston University" in driver.title

    # Input username
    elem_username = driver.find_element(by="name", value="j_username")
    elem_username.clear()
    elem_username.send_keys(os.getenv("BU_USERNAME"))

    # Input password
    elem_password = driver.find_element(by="name", value="j_password")
    elem_password.clear()
    elem_password.send_keys(os.getenv("BU_PASSWORD"))

    # Submit login form
    elem_button = driver.find_element(by="class name", value="input-submit")
    elem_button.click()

    assert "Home" in driver.title


def get_badge(driver):
    assert "Home" in driver.title

    elem_badge_button = driver.find_element(by="id", value="showQuarantineBadge")
    elem_badge_button.click()

    sleep(1)

    timestamp = datetime.date.today().strftime("%y%m%d")
    filename = f"{timestamp}.png"
    driver.save_screenshot(filename)

    return timestamp


def init_icloud():
    api = PyiCloudService(apple_id=os.getenv("APPLE_USERNAME"), password=os.getenv("APPLE_PASSWORD"))

    if api.requires_2fa:
        print("Two-factor authentication required.")
        code = input("Enter the code you received of one of your approved devices: ")
        result = api.validate_2fa_code(code)
        print("Code validation result: %s" % result)

        if not result:
            print("Failed to verify security code")
            sys.exit(1)

        if not api.is_trusted_session:
            print("Session is not trusted. Requesting trust...")
            result = api.trust_session()
            print("Session trust result %s" % result)

            if not result:
                print("Failed to request trust. You will likely be prompted for the code again in the coming weeks")

    return api


def upload_badge(api, timestamp):
    with open(f"{timestamp}.png", 'rb') as file_in:
        api.drive[os.getenv("ICLOUD_FOLDER_NAME")].upload(file_in)


def cleanup_files(timestamp):
    os.remove(f"{timestamp}.png")


def main():
    load_dotenv()

    driver = init_driver()
    login(driver=driver)
    timestamp = get_badge(driver=driver)
    driver.close()

    icloud_api = init_icloud()
    upload_badge(api=icloud_api, timestamp=timestamp)
    cleanup_files(timestamp=timestamp)


if __name__ == '__main__':
    main()
