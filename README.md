# BU Badge Collector
A script to grab a BU account's green badge and upload it to iCloud Drive

## Setup

1. Run `pip install -r requirements.txt`
2. Rename `.env.example` to `.env`
3. Fill in your BU/Apple username and password
4. In your iCloud Drive, create a folder for the badge to be uploaded to
5. Set `ICLOUD_FOLDER_NAME` to the name of the folder you just created
6. [Download chromedriver](https://chromedriver.chromium.org/downloads)
7. Set `CHROMEDRIVER_PATH` to the path for the chromedriver you just downloaded
8. Run `main.py`

## Apple 2FA
If you have Apple 2FA enabled, you will be prompted to enter the 2FA code.
It will be stored and valid until Apple revokes it. **2SA is currently not supported.**