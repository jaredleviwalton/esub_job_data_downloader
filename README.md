# Construction job data scraper for eSUB website

- [Construction job data scraper for eSUB website](#construction-job-data-scraper-for-esub-website)
  - [Basic Info](#basic-info)
  - [Copyright](#copyright)
  - [Requirements](#requirements)
  - [How to run](#how-to-run)
    - [Username and Password](#username-and-password)
    - [To Run](#to-run)

## Basic Info

This will scrape the website app.esub.com for the following data:

- Project
  - Project Inbox
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found). This includes attachments found in each email.
  - Issues
    - Excel sheet listing items available on eSUB
    - A folder listing issues (Note: This does not have an associated folder).
- Construction Docs
  - Field Notes
    - A folder containing all items found on the field notes page (Note: This does not have a Excel sheet).
  - Daily Reports
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Requests for Information
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Submittals
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Correspondence log
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Drawing Sets
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Contacts
    - Excel sheet listing job contact information (Note: This does not have an associated folder).
- Job Cost Docs
  - Change Order Requests
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Purchase Orders
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Subcontracts
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Subcontract Change Orders
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
  - Pay Application Log
    - Excel sheet listing items available on eSUB
    - A folder containing all items listed in the Excel sheet (Note: This folder may be empty if no items were found).
- Files
  - Project Files
    - A folder containing all items found on the field notes page (Note: This does not have a Excel sheet).
  - Company Files
    - A folder containing all items found on the field notes page (Note: This does not have a Excel sheet).

## Copyright

MIT License

Copyright (c) 2022 Jared Walton <[jared.levi.walton@gmail.com](jared.levi.walton@gmail.com)>

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

## Requirements

- Windows OS
- Python 3.9+  
- pip
- Packages in requirements.txt
- chromedriver binary (download the one to match your installed chrome version)
- Excel

## How to run

### Username and Password

1. Create a file: ```src\_secrets.py```
2. In it add the following, substituting the correct username and password.

    ```python
    USER_NAME = "SomeName@somedomain.com"
    USER_PASS = "monkey123_password!"
    ```

3. Update the following lines in ```src\users_and_passwords.py``` with your info.

    ```python
    LOGIN_URL = "https://app.esub.com/login"
    PROJECTS_URL = "https://app.esub.com/project"

    PROJECT_URLS = [
        "https://app.esub.com/project/10115",
        "https://app.esub.com/project/1",
        "https://app.esub.com/project/10257",
        "https://app.esub.com/project/10100",
        "https://app.esub.com/project/10103",
        "https://app.esub.com/project/10133",
        "https://app.esub.com/project/10104",
        "https://app.esub.com/project/10215",
        "https://app.esub.com/project/10072",
        ...
        "https://app.esub.com/project/10096",
    ]
    ```
  
4. If on a smaller screen (like a laptop) change ```FULL_SCREEN_CHROME = False``` to ```FULL_SCREEN_CHROME = True``` in ```src\users_and_passwords.py```

### To Run

1. Make sure the chromedriver is in your system path.
2. Make sure Python 3.9 or better is installed.
3. Make sure pip is installed
4. Create a virtual environment

    ```shell
    python3 -m venv .venv
    ```

5. Install dependencies

    ```shell
    pip install -r requirements.txt
    ```

6. Set your computer power settings such that it will never sleep, lock or turn the monitor off.
7. If using vsCode (and I recommend you do) press F5 or start debugging the file located at: src\esub_project_download.py
8. Otherwise run the following command

    ```shell
    python3 src\esub_project_download.py
    ```

9. You will see multiple chrome windows open up. **DO NOT** interact with it, don't even scroll. JUST LET IT RUN. It will likely take along time, depending on the number of jobs. Example: for about 300 jobs on a 10 core system it took about 10 hours.

10. After completing check ```validation.log``` and ensure that there are no entries, if there are address them.

11. Also check the ```remaining``` folder, if there are any files in it, check the ```debug``` folder for info on how to address these projects that were not downloaded.
