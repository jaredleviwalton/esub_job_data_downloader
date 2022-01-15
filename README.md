# Construction job data scraper for eSUB website

A project data scraper for apps.eSUB.com

---

## Table of Contents

- [Construction job data scraper for eSUB website](#construction-job-data-scraper-for-esub-website)
  - [Table of Contents](#table-of-contents)
  - [Copyright](#copyright)
  - [Requirements](#requirements)
  - [How to run](#how-to-run)
    - [Config, Username and Password](#config-username-and-password)
    - [To Run](#to-run)
  - [Payload Info](#payload-info)

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

### Config, Username and Password

1. Create a file: ```src\_secrets.py```
2. In it add the following, substituting the correct username and password.

    ```python
    USER_NAME = "SomeName@somedomain.com"
    USER_PASS = "monkey123_password!"
    ```

3. If on a smaller screen (like a laptop) in the file ```src\users_and_passwords.py``` change the following

    ```python
    FULL_SCREEN_CHROME = False
    ```

    to

    ```python
    FULL_SCREEN_CHROME = True
    ```

### To Run

0. Clone the git repo to a non-cloud syncing folder. This may download thousands of files amounting to tens of gigabytes, and will overload OneDrive and cause data corruption.
1. Make sure chrome is installed.
2. Make sure  chromedriver (matching the version of chrome you have instaslled) is in your system path. If you are using vsCode and opend the '.code-workspace' simply downloading and placing 'chromedriver.exe' in the same folder as the workspace file should work.
3. Make sure Python 3.9 or better is installed.
4. Make sure pip is installed
5. Make sure excel is installed and activated
6. Create a virtual environment

    ```shell
    python3 -m venv .venv
    ```

7. Install dependencies

    ```shell
    pip install -r requirements.txt
    ```

8. Set your computer power settings such that it will never sleep, lock or turn the monitor off.
9. If using vsCode (and I recommend you do) press F5 or start debugging the file located at: src\esub_project_download.py
10. Otherwise run the following command

    ```shell
    python3 src\esub_project_download.py
    ```

11. You will see multiple chrome windows open up. **DO NOT** interact with it, don't even scroll. JUST LET IT RUN. It will likely take along time, depending on the number of jobs. Example: for about 300 jobs on a 10 core system it took about 10 hours.

12. After completing, check the ```payload_verification.log``` and ensure that there are no entries, if there are address them.

13. Also check the ```remaining``` folder, if there are any files in it, check the ```debug``` folder for info on how to address the projects that were not downloaded.

## Payload Info

This will scrape the website app.esub.com for the following data and place it into the ```payload``` folder:

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

