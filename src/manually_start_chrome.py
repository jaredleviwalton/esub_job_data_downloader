import json
from selenium import webdriver
CHROME_DOWNLOAD_FOLDER_PATH = r"C:\Users\jawalking\tmp"
chrome_options = webdriver.ChromeOptions()

# For printing as PDF
settings = {
    "recentDestinations": [{
        "id": "Save as PDF",
        "origin": "local",
        "account": "",
    }],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}
prefs = {
    'download.default_directory': CHROME_DOWNLOAD_FOLDER_PATH,  # our temp download location
    "download.prompt_for_download": False,  # for saving pdf files
    "download.directory_upgrade": True,  # for saving pdf files
    "plugins.always_open_pdf_externally": True,  # Don't open PDF in chrome
    'printing.print_preview_sticky_settings.appState': json.dumps(settings),  # for pdf printing
    'savefile.default_directory': CHROME_DOWNLOAD_FOLDER_PATH,  # for pdf printing
}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--kiosk-printing')  # for pdf printing
driver_session = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
print(f"{driver_session.command_executor._url=}")  # We'll need this for keeping this session
print(f'{driver_session.session_id=}')  # We'll need this for keeping this session
