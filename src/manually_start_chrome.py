"""
MIT License

Copyright (c) 2022 Jared Walton <jared.levi.walton@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
from selenium import webdriver

CHROME_DOWNLOAD_FOLDER_PATH = r"C:\Users\jawalking\tmp"
chrome_options = webdriver.ChromeOptions()

# For printing as PDF
settings = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": "",
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2,
}
prefs = {
    "download.default_directory": CHROME_DOWNLOAD_FOLDER_PATH,  # our temp download location
    "download.prompt_for_download": False,  # for saving pdf files
    "download.directory_upgrade": True,  # for saving pdf files
    "plugins.always_open_pdf_externally": True,  # Don't open PDF in chrome
    "printing.print_preview_sticky_settings.appState": json.dumps(settings),  # for pdf printing
    "savefile.default_directory": CHROME_DOWNLOAD_FOLDER_PATH,  # for pdf printing
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--kiosk-printing")  # for pdf printing
driver_session = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
print(f"{driver_session.command_executor._url=}")  # We'll need this for keeping this session
print(f"{driver_session.session_id=}")  # We'll need this for keeping this session
