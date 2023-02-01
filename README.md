# Construction job data scraper for eSUB website

A project data scraper for apps.eSUB.com

---

## Table of Contents

- [Construction job data scraper for eSUB website](#construction-job-data-scraper-for-esub-website)
  - [Table of Contents](#table-of-contents)
  - [Copyright](#copyright)
  - [Requirements](#requirements)
  - [Recomended](#recomended)
  - [How to run](#how-to-run)
    - [Config, Username and Password](#config-username-and-password)
    - [To Run](#to-run)
  - [Payload Info](#payload-info)
    - [File Structure and Naming](#file-structure-and-naming)
    - [Project Items Gathered](#project-items-gathered)

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

- [Windows OS](https://www.microsoft.com/software-download/windows11)
- [Python 3.9+](https://www.python.org/downloads/)
- [pip](https://pypi.org/project/pip/)
- [Packages in requirements.txt](requirements.txt)
- [Chrome web browser](https://www.google.com/chrome/)
- [chromedriver binary](https://chromedriver.chromium.org/downloads) (download the one to match your installed chrome version)
- [Excel](https://www.microsoft.com/en-us/microsoft-365/excel)

## Recomended

- [Microsoft Visual Studio Code](https://code.visualstudio.com/)

## How to run

### Config, Username and Password

1. Create a file: ```src\_secrets.py```
2. In it add the following, substituting the correct username and password.

    ```python
    USER_NAME = "SomeName@somedomain.com"
    USER_PASS = "monkey123_password!"
    ```

3. If on a smaller screen (like a laptop) in the file ```src\config.py``` change the following

    ```python
    FULL_SCREEN_CHROME = False
    ```

    to

    ```python
    FULL_SCREEN_CHROME = True
    ```

4. By default it will utilize all cores on your system, an 8-core system will result in 8 chrome windows each pulling data from a different project. This can be CPU and network intensive. If you wish to only allocate one or a few cores, modify the following line in ```src\config.py```, by replacing 'None' with '1' or whatever number of cores you wish.

    ```python
    NUM_CONCURRENT_SESSIONS = None
    ```

### To Run

1. Clone the git repo to a non-cloud syncing folder. This may download thousands of files amounting to tens of gigabytes, and will overload OneDrive and may cause data corruption.
2. Make sure chrome is installed.
3. Make sure  chromedriver (matching the version of chrome you have instaslled) is in your system path. If you are using vsCode and opend the '.code-workspace' simply downloading and placing 'chromedriver.exe' in the same folder as the workspace file should work.
4. Make sure Python 3.9 or better is installed.
5. Make sure pip is installed
6. Make sure excel is installed and activated
7. Create a virtual environment

    ```shell
    python3 -m venv .venv
    ```

8. Ensure that you are in the virtual environment. You may need to [set the execution policy for powershell](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.security/set-executionpolicy?view=powershell-7.2). Run the following command, then close and re-open the shell session.

    ```powershell
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```

9. Install dependencies

    ```shell
    pip install -r requirements.txt
    ```

10. Set your computer power settings such that it will never sleep, lock or turn the monitor off.
11. If using vsCode (and I recommend you do) press F5 to run the file ```src\download_project_files.py```
12. Otherwise run the following command

    ```shell
    python3 src\download_project_files.py
    ```

13. You will see one or more chrome windows open up. **DO NOT** interact with it, don't even scroll. JUST LET IT RUN. It could take along time depending on the number of jobs and number of job files. Example: for about 300 jobs on a 10 core system it took about 10 hours.

14. After completing, check the ```payload_verification.log``` and ensure that there are no entries, if there are, address them.

15. Also check the ```remaining``` folder, if there are any files in it, check the ```debug``` folder for info on how to address the projects that were not downloaded.

## Payload Info

Data pulled from the will be placed into the ```payload``` folder, with each folder representing a project

### File Structure and Naming

- Job folder naming:
  - Example: ‘10115 - 198-1 - Some Project Name’ where ‘10115’ is the job ID from the URL: [https://app.esub.com/project/**10115**](https://app.esub.com/project/10115) and the rest is the job number and name from the eSUB summary page

- Each job folder follows the tab structure as is listed above and from the site
- Emails:
  - Each email name has the following structure:
    - Example: '10256 - Re [EXT] Some Project Name project PO No 198-1-1' where '10256' is the email Number listed in the excel sheet and also on the jobs Project Inbox page the rest is the email subject.  
    - Attachments from an email bear the same name and number as their parent email, but also include ' – Attachment – ' followed by the attachments name.
      - Example: '10256 - Re [EXT] Some Project Name project PO No 198-1-1 - Attachment - P.198-1-1.1242018.1502.pdf'
- If a file with the same name is downloaded, the subsequent ones will be appended with five "-" followed by twelve unique characters.
  - Example: 'S.018-65-1-----f8253b1aa2c7.pdf'

### Project Items Gathered

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
