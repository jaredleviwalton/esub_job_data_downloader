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
from multiprocessing import Pool, cpu_count
from multiprocessing.context import Process
import os
import pathlib
import random
import re
import timeit
from time import sleep
import traceback
from typing import List, Tuple
from shutil import Error, get_terminal_size, rmtree
from uuid import uuid1, uuid4
from urllib.parse import quote as url_quote
from urllib.request import urlretrieve
from selenium import webdriver

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Remote
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

import users_and_passwords as unp


class eSUB:
    PROJECT_URLS = unp.PROJECT_URLS

    LOGIN_URL = unp.LOGIN_URL
    PROJECTS_URL = unp.PROJECTS_URL

    CHROME_DOWNLOAD_FOLDER_PATH = unp.CHROME_DOWNLOAD_FOLDER_PATH

    DOWNLOAD_BASE_FOLDER = unp.DOWNLOAD_BASE_FOLDER

    # existing driver session for debugging and when it breaks
    # update as neededs
    EXISTING_SESSION_URL = "http://localhost:55185"
    EXISTING_SESSION_ID = "a43ba8c76f344a3f064797247aa41ae4"

    def __init__(
        self,
        project_url,
        use_existing_session: Tuple[str, str] = None,
        my_url_list=None,
        download_proj=True,
    ):

        # setup folder paths
        pathlib.Path(self.CHROME_DOWNLOAD_FOLDER_PATH).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.DOWNLOAD_BASE_FOLDER).mkdir(parents=True, exist_ok=True)

        # Used for multiprocessing
        self.CHROME_DOWNLOAD_FOLDER_PATH = os.path.join(self.CHROME_DOWNLOAD_FOLDER_PATH, f"{uuid4()}")
        if os.path.exists(self.CHROME_DOWNLOAD_FOLDER_PATH):
            print("!!!!!!!!!! UUID4 collision !!!!!!!!!!!!!!!")
            return
        else:
            pathlib.Path(self.CHROME_DOWNLOAD_FOLDER_PATH).mkdir(parents=True, exist_ok=True)

        if my_url_list is not None:
            self.PROJECT_URLS = my_url_list

        # Setup chromedriver
        if use_existing_session is not None:
            self.driver_session = Remote(command_executor=self.EXISTING_SESSION_URL, desired_capabilities={})
            self.driver_session.close()
            self.driver_session.session_id = self.EXISTING_SESSION_ID
        else:
            chrome_options = ChromeOptions()

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
                "download.default_directory": self.CHROME_DOWNLOAD_FOLDER_PATH,  # our temp download location
                "download.prompt_for_download": False,  # for saving pdf files
                "download.directory_upgrade": True,  # for saving pdf files
                "plugins.always_open_pdf_externally": True,  # Don't open PDF in chrome
                "printing.print_preview_sticky_settings.appState": json.dumps(settings),  # for pdf printing
                "savefile.default_directory": self.CHROME_DOWNLOAD_FOLDER_PATH,  # for pdf printing
            }
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # suppress dev tools loging
            chrome_options.add_argument("--kiosk-printing")  # for pdf printing
            if unp.FULL_SCREEN_CHROME:
                chrome_options.add_argument("--kiosk")
            chrome_options.add_argument("log-level=3")  # ignore warnings
            chrome_options.add_argument("--new-window")
            self.driver_session = Chrome("chromedriver", options=chrome_options)

            self.MAIN_URL = self.driver_session.command_executor._url
            self.MAIN_SESSION_ID = self.driver_session.session_id
            # print(f"{self.driver_session.command_executor._url=}")  # We'll need this for keeping this session
            # print(f"{self.driver_session.session_id=}")  # We'll need this for keeping this session
            # print("\n")

            self._login()

        if download_proj:
            self.download_project(project_url)

    def _login(self) -> None:
        self.driver_session.get(self.LOGIN_URL)

        sleep(7)

        self.driver_session.find_element(By.ID, "txtUsername").send_keys(unp.USER_NAME)
        self.driver_session.find_element(By.ID, "txtPassword").send_keys(unp.USER_PASS)

        self.driver_session.find_element(By.ID, "btnLogin").click()

        sleep(5)

    def get_project_page(self, project_url):
        # Load the project page
        self.driver_session.get(project_url)
        self.project_url = project_url

        # get the url id number to help with non-unique names
        url_id = os.path.basename(project_url)

        # get the project name
        sleep(7)
        project_name = (
            str(self.driver_session.find_elements(By.CLASS_NAME, "es-project-summary__title")[0].text)
            .strip(r"business")
            .strip(r"keybaord_arrow_down")
            .strip("\n")
        )

        # windows path safe project name
        project_name = self._get_windows_path_safe_string(project_name)

        # the project download folder is the url id + the project name
        self.project_download_folder = os.path.join(self.DOWNLOAD_BASE_FOLDER, f"{url_id} - {project_name}")
        # print(self.project_url)
        # print(self.project_download_folder)

        sleep(300)

    # Use self.project_urls instead
    def get_project_urls(self) -> List[str]:
        self.driver_session.get(self.PROJECTS_URL)
        sleep(7)

        # scroll down the page to force all projects to populate
        # TODO: this has problems, need to manually scroll or move mouse to middle
        # self._scroll_down_page()

        # action = ActionChains(self.driver_session)

        # for _ in range(6):
        #     project_elements = self.driver_session.find_elements(By.CSS_SELECTOR, ".project-card")
        #     action.move_to_element(project_elements[-1])
        #     action.perform()
        #     location = project_elements[-1].location
        #     sleep(1)

        i = 1
        screen_height = self.driver_session.execute_script("return window.screen.height;")
        while True:
            current_element = self.driver_session.find_elements(By.CSS_SELECTOR, ".project-card")[-1]
            # scroll one screen height each time
            self.driver_session.execute_script(
                "{element}.scrollTo(0, {screen_height}*{i});".format(
                    element=current_element, screen_height=screen_height, i=i
                )
            )
            i += 1
            sleep(5)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = self.driver_session.execute_script("return document.body.scrollHeight;")
            # Break the loop when the height we need to scroll to is larger than the total scroll height
            if (screen_height) * i > scroll_height:
                break

        project_urls = []
        for project in self.driver_session.find_elements(By.CSS_SELECTOR, ".project-card"):
            project_urls.append(project.get_attribute("href"))

        return project_urls

    def _get_windows_path_safe_string(self, string) -> str:
        return re.sub(r'[\\/\:*"<>\|\?]', "", string)

    def _refresh_proj_page(self):
        self.driver_session.get(self.project_url)
        sleep(7)
        sleep(7)

    def download_files(self) -> None:

        # for project_url in self.PROJECT_URLS:
        for project_url in tqdm(self.PROJECT_URLS):
            print("\n")

            # Load the project page
            self.driver_session.get(project_url)
            self.project_url = project_url

            # get the url id number to help with non-unique names
            url_id = os.path.basename(project_url)

            # get the project name
            sleep(5)
            project_name = (
                str(self.driver_session.find_elements(By.CLASS_NAME, "es-project-summary__title")[0].text)
                .strip(r"business")
                .strip(r"keybaord_arrow_down")
                .strip("\n")
            )

            # windows path safe project name
            project_name = self._get_windows_path_safe_string(project_name)

            # the project download folder is the url id + the project name
            self.project_download_folder = os.path.join(self.DOWNLOAD_BASE_FOLDER, f"{url_id} - {project_name}")
            print(self.project_url)
            print(self.project_download_folder)
            print(
                f"\nProc-{os.path.basename(self.CHROME_DOWNLOAD_FOLDER_PATH)}: \t {self.project_url} \t -> \t {self.project_download_folder}"
            )
            pathlib.Path(self.project_download_folder).mkdir(parents=True, exist_ok=True)

            # fmt: off

            # Project tab
            self._get_emails("Project", "Project Inbox", log_info=True)
            self._get_typical_page_docs("Project", "Contacts", download_files=False, log_info=True)
            self._get_typical_page_docs("Project", "Issues", log_info=True)

            # Construction Docs tab
            self._get_typical_page_docs("Construction Docs", "Field Notes", log_info=True)
            self._get_typical_page_docs("Construction Docs", "Daily Reports", log_info=True)
            self._get_typical_page_docs("Construction Docs", "Requests For Information", log_info=True)
            self._get_typical_page_docs("Construction Docs", "Submittals", log_info=True)
            self._get_typical_page_docs("Construction Docs", "Meeting Minutes", log_info=True)
            self._get_typical_page_docs("Construction Docs", "Equipment Rental", log_info=True)
            self._get_typical_page_docs("Construction Docs", "Correspondence Log", log_info=True)
            self._get_typical_page_docs("Construction Docs", "Drawing Sets", log_info=True)

            # Job Cost Docs tab
            self._get_typical_page_docs("Job Cost Docs", "Change Order Requests", log_info=True)
            self._get_typical_page_docs("Job Cost Docs", "Purchase Orders", log_info=True)
            self._get_typical_page_docs("Job Cost Docs", "Subcontracts", log_info=True)
            self._get_typical_page_docs("Job Cost Docs", "Subcontract Change Orders", log_info=True)
            self._get_typical_page_docs("Job Cost Docs", "Pay Applications", log_info=True)

            # Files tab
            self._get_files("Files", "Project Files", log_info=True)
            self._get_files("Files", "Company Files", log_info=True)

            # fmt: on

            for i in range(get_terminal_size()[0]):
                print("=", end="")
            print("\n")

    def download_project(self, project_url) -> None:
        try:
            # for project_url in self.PROJECT_URLS:
            # for project_url in tqdm(self.PROJECT_URLS):
            # print("\n")

            # Load the project page
            self.driver_session.get(project_url)
            self.project_url = project_url

            # get the url id number to help with non-unique names
            url_id = os.path.basename(project_url)

            # get the project name
            sleep(7)
            project_name = (
                str(self.driver_session.find_elements(By.CLASS_NAME, "es-project-summary__title")[0].text)
                .strip(r"business")
                .strip(r"keybaord_arrow_down")
                .strip("\n")
            )

            # windows path safe project name
            project_name = self._get_windows_path_safe_string(project_name)

            # the project download folder is the url id + the project name
            self.project_download_folder = os.path.join(self.DOWNLOAD_BASE_FOLDER, f"{url_id} - {project_name}")
            # print(self.project_url)
            # print(self.project_download_folder)
            # print(
            #     f"\nProc-{os.path.basename(self.CHROME_DOWNLOAD_FOLDER_PATH)}: \t {self.project_url} \t -> \t {self.project_download_folder}"
            # )
            pathlib.Path(self.project_download_folder).mkdir(parents=True, exist_ok=True)

            # fmt: off

            # Project tab
            self._get_emails("Project", "Project Inbox", log_info=False)
            self._get_typical_page_docs("Project", "Contacts", download_files=False, log_info=False)
            self._get_typical_page_docs("Project", "Issues", log_info=False)

            # Construction Docs tab
            self._get_typical_page_docs("Construction Docs", "Field Notes", log_info=False)
            self._get_typical_page_docs("Construction Docs", "Daily Reports", log_info=False)
            self._get_typical_page_docs("Construction Docs", "Requests For Information", log_info=False)
            self._get_typical_page_docs("Construction Docs", "Submittals", log_info=False)
            self._get_typical_page_docs("Construction Docs", "Meeting Minutes", log_info=False)
            self._get_typical_page_docs("Construction Docs", "Equipment Rental", log_info=False)
            self._get_typical_page_docs("Construction Docs", "Correspondence Log", log_info=False)
            self._get_typical_page_docs("Construction Docs", "Drawing Sets", log_info=False)

            # Job Cost Docs tab
            self._get_typical_page_docs("Job Cost Docs", "Change Order Requests", log_info=False)
            self._get_typical_page_docs("Job Cost Docs", "Purchase Orders", log_info=False)
            self._get_typical_page_docs("Job Cost Docs", "Subcontracts", log_info=False)
            self._get_typical_page_docs("Job Cost Docs", "Subcontract Change Orders", log_info=False)
            self._get_typical_page_docs("Job Cost Docs", "Pay Applications", log_info=False)

            # Files tab
            self._get_files("Files", "Project Files", log_info=False)
            self._get_files("Files", "Company Files", log_info=False)

            # fmt: on

            # for i in range(get_terminal_size()[0]):
            #     print("=", end="")
            # print("\n")
        except:
            debug_log = "\n"
            debug_log += f"{self.project_url}"
            debug_log += f"{self.project_download_folder}"
            debug_log += "\n"
            debug_log += f"{traceback.format_exc()}"
            debug_log += "\n"
            debug_log += f"{self.project_url}"
            debug_log += f"{self.project_download_folder}"
            debug_log += "\n"

            for _ in range(get_terminal_size()[0]):
                print("=", end="")
            print(debug_log)
            for _ in range(get_terminal_size()[0]):
                print("=", end="")

            debug_log_path = os.path.join(
                unp.DEBUG_PATH, f"DEBUG_project_url_num_{os.path.basename(project_url)}_{uuid1()}.txt"
            )
            with open(debug_log_path, "w") as fh:
                fh.write(debug_log)

            # Cleanup
            rmtree(self.project_download_folder)
            rmtree(self.CHROME_DOWNLOAD_FOLDER_PATH)
            self.driver_session = None
        else:
            rmtree(self.CHROME_DOWNLOAD_FOLDER_PATH)
            os.remove(os.path.join(unp.REMAINING_PATH, f"project_url_num_{os.path.basename(project_url)}"))
            self.driver_session = None

    def _get_files(self, menu_name, sub_job_cost_doc_item, log_info=False):
        self._refresh_proj_page()
        if log_info:
            my_vars = list(locals().values())
            print(f"\t\t{my_vars[1]} -> {my_vars[2]}")

        # get the files dropdown and click on it
        sleep(5)
        for dropdown in self.driver_session.find_elements(By.CSS_SELECTOR, ".es-dropdown-menu-trigger"):
            if menu_name == dropdown.text:
                dropdown.click()

                sleep(5)

                # get the projects files sub menu item and click on it
                for item in self.driver_session.find_elements(By.CSS_SELECTOR, ".es-dropdown-menu__item"):
                    if sub_job_cost_doc_item == item.text:
                        item.click()
                        break

                pathlib.Path(os.path.join(self.project_download_folder, menu_name, sub_job_cost_doc_item)).mkdir(
                    parents=True, exist_ok=True
                )

                self._download_project_files(menu_name, sub_job_cost_doc_item)

    def _get_emails(self, tab_name, sub_job_cost_doc_item, log_info=False):
        self._refresh_proj_page()
        if log_info:
            my_vars = list(locals().values())
            print(f"\t\t{my_vars[1]} -> {my_vars[2]}")

        # get the files dropdown and click on it
        sleep(5)
        menus = self.driver_session.find_elements(By.CSS_SELECTOR, ".es-dropdown-menu-trigger")
        for dropdown in menus:
            if tab_name in str(dropdown.accessible_name):
                dropdown.click()

                sleep(5)

                # get the projects files sub menu item and click on it
                sub_menus = self.driver_session.find_elements(By.CSS_SELECTOR, ".es-dropdown-menu__item")
                for item in sub_menus:
                    if sub_job_cost_doc_item in item.text:
                        item.click()
                        break

                sleep(10)
                pathlib.Path(os.path.join(self.project_download_folder, tab_name)).mkdir(parents=True, exist_ok=True)

                # get excel summary
                on_mouse_over_items = self.driver_session.find_elements(By.XPATH, '//*[@name="IconXLS1"]')
                for item in on_mouse_over_items:
                    if "Excel" in item.text or len(on_mouse_over_items) == 1:

                        # Clean up any existing files first before downloading
                        files = list(pathlib.Path(self.CHROME_DOWNLOAD_FOLDER_PATH).glob("**/*"))
                        for file in files:
                            os.remove(file)

                        # download
                        item.click()
                        self._wait_for_chrome_downloads(number_of_files=1)

                        # only expect one file
                        files = os.listdir(self.CHROME_DOWNLOAD_FOLDER_PATH)[0]
                        pathlib.Path(os.path.join(self.CHROME_DOWNLOAD_FOLDER_PATH, files)).replace(
                            os.path.join(self.project_download_folder, tab_name, f"{sub_job_cost_doc_item}.xls")
                        )
                        # sleep(2)
                        break

                # download files
                self._save_email(tab_name, sub_job_cost_doc_item)

                break

    def _get_typical_page_docs(self, menu_name, sub_menu_name, download_files=True, log_info=False):
        self._refresh_proj_page()
        if log_info:
            my_vars = list(locals().values())
            print(f"\t\t{my_vars[1]} -> {my_vars[2]}")

        # get the files dropdown and click on it
        sleep(5)
        menus = self.driver_session.find_elements(By.CSS_SELECTOR, ".es-dropdown-menu-trigger")
        for dropdown in menus:
            if menu_name in str(dropdown.accessible_name):
                dropdown.click()

                # get the projects files sub menu item and click on it
                sleep(3)
                sub_menus = self.driver_session.find_elements(By.CSS_SELECTOR, ".es-dropdown-menu__item")
                for item in sub_menus:
                    if sub_menu_name in item.text:
                        item.click()
                        break

                sleep(5)
                # self._wait_for(
                #     css_selector="[onmouseover=\"window.status='Go to eSUB Inc. corporate site';return true;\"]"
                # )
                pathlib.Path(os.path.join(self.project_download_folder, menu_name)).mkdir(parents=True, exist_ok=True)

                # get excel summary
                on_mouse_over_items = self.driver_session.find_elements(By.XPATH, '//*[@name="IconXLS1"]')
                for item in on_mouse_over_items:
                    if "Excel" in item.text or len(on_mouse_over_items) == 1:

                        # Clean up any existing files first before downloading
                        files = list(pathlib.Path(self.CHROME_DOWNLOAD_FOLDER_PATH).glob("**/*"))
                        for file in files:
                            os.remove(file)

                        # download
                        item.click()
                        self._wait_for_chrome_downloads(number_of_files=1)

                        # We expect only one file
                        files = os.listdir(self.CHROME_DOWNLOAD_FOLDER_PATH)[0]

                        # move to correct location
                        pathlib.Path(os.path.join(self.CHROME_DOWNLOAD_FOLDER_PATH, files)).replace(
                            os.path.join(self.project_download_folder, menu_name, f"{sub_menu_name}.xls")
                        )

                        break  # We are done here, don't try to process inactive menu items

                if download_files:
                    self._download_pdf_files(menu_name, sub_menu_name)

                break  # We are done here, don't try to process inactive menu items

    def _wait_for_chrome_downloads(self, timeout=1800, number_of_files=None) -> None:
        seconds = 0
        keep_waiting = True

        while keep_waiting and seconds < timeout:
            sleep(1)

            keep_waiting = False

            # Get contents of donload folder
            files = os.listdir(self.CHROME_DOWNLOAD_FOLDER_PATH)

            # if we are waiting for a specific number of files, check how many we have
            if number_of_files and len(files) != number_of_files:
                keep_waiting = True

            # if the file ends with .crdownload wait
            # there was a .tmp file that messed up a download so add that,
            # but I don't know why that would be...
            for file_name in files:
                if file_name.endswith(".crdownload") or file_name.endswith(".tmp"):
                    keep_waiting = True

            # Wait another second
            seconds += 1

        # TODO: Throw error or do something to handle timeout

    def _save_email(self, tab_name, sub_job_cost_doc_item):

        # Setup project email download path
        download_path = os.path.join(self.project_download_folder, tab_name, sub_job_cost_doc_item)
        pathlib.Path(download_path).mkdir(parents=True, exist_ok=True)

        items_to_download = self.driver_session.find_elements(
            By.CSS_SELECTOR, '[alt="View this Incoming Correspondence"]'
        )
        email_numbers = self.driver_session.find_elements(By.CSS_SELECTOR, '[alt="Created from Incoming Email"]')

        # For some reason getting these items in reverse order causes hangs...
        # for item, number_element in zip(items_to_download[::-1], email_numbers[::-1]):
        for item, number_element in zip(items_to_download, email_numbers):
            email_number = number_element.find_element(By.XPATH, "../..").text

            item.click()
            sleep(5)

            # Clean up any existing files first before downloading
            files = list(pathlib.Path(self.CHROME_DOWNLOAD_FOLDER_PATH).glob("**/*"))
            for file in files:
                os.remove(file)

            # Switch to just oppend tab
            self.driver_session.switch_to.window(self.driver_session.window_handles[-1])

            # The name is the only element with this bg class on the page
            email_name = self.driver_session.find_elements(By.XPATH, '//*[@class="bgcolor3"]')[0].accessible_name
            email_name = self._get_windows_path_safe_string(email_name)
            email_save_path = os.path.join(download_path, f"{email_number} - {email_name}.pdf")

            # Print email and move to project email folder
            if not os.path.exists(email_save_path):
                self.driver_session.execute_script("window.print();")
                sleep(5)
                files = os.listdir(self.CHROME_DOWNLOAD_FOLDER_PATH)[0]  # only one file expected
                pathlib.Path(os.path.join(self.CHROME_DOWNLOAD_FOLDER_PATH, files)).replace(email_save_path)

            # Attachment links are next to these icons, so get all of them
            attachment_icon_elements = self.driver_session.find_elements(
                By.CSS_SELECTOR, '[src="/TRACKpoint/images/icons/attachment.png"]'
            )
            for attachment_icon_element in attachment_icon_elements:

                # get the parent and sibling element(s) for the attachment icon
                # sibling at index 0 is the icon
                # sibling at index 1 is the attachment name
                # sibling at index 2 is the download link
                parent_element = attachment_icon_element.find_element(By.XPATH, "../..")
                sibling_elements = parent_element.find_elements(By.XPATH, "*")

                attachment_name = sibling_elements[1].text
                attachment_name = self._get_windows_path_safe_string(attachment_name)

                down_url = sibling_elements[2].find_elements(By.XPATH, "*")[0].get_attribute("href")

                save_path = os.path.join(
                    download_path, f"{email_number} - {email_name} - Attachment - {attachment_name}"
                )

                # Download attachment
                urlretrieve(url_quote(down_url, safe="/:?&()"), save_path)

            # Close Tab and switch context to main tab
            self.driver_session.close()
            self.driver_session.switch_to.window(self.driver_session.window_handles[0])

        # if there is a next page, download that
        next_page = self.driver_session.find_elements(By.XPATH, "//*[@onmouseover]")
        for item in next_page:
            if item.accessible_name == "Go to next page":
                item.click()

                # recuse for each next page
                self._save_email(tab_name, sub_job_cost_doc_item)

                break  # probably don't need this but don't want to test it

    def _download_pdf_files(self, tab_name, sub_job_cost_doc_item):

        sleep(3)

        project_files_download_path = os.path.join(self.project_download_folder, tab_name, sub_job_cost_doc_item)
        pathlib.Path(project_files_download_path).mkdir(parents=True, exist_ok=True)

        # Get all the download as PDF items
        items_to_download = self.driver_session.find_elements(By.CSS_SELECTOR, '[alt="Download as PDF"]')

        # For some reason this wants things from the bottom up, or it hangs.
        for item in items_to_download[::-1]:
            try:
                item.click()
            except:
                # This is an attempt to handle an edge case case < 2%
                # where the help icon is obscuring the download button (only on Field Notes)
                # But it causes a full halt to the run.

                # Get body and arrow key down
                # TODO: Use this to get all projects from main page
                main = self.driver_session.find_element(By.CSS_SELECTOR, "body")
                main.send_keys(Keys.DOWN)
                main.send_keys(Keys.DOWN)
                sleep(3)

                # Re-find all download elements, match with the current item and click it
                # if we don't find it raise and exception
                new_download_item_list = self.driver_session.find_elements(By.CSS_SELECTOR, '[alt="Download as PDF"]')

                found = False
                for new_item in new_download_item_list:
                    if new_item.id == item.id:
                        new_item.click()
                        found = True
                        break

                if not found:
                    raise Exception("Attempting to find a matching item failed.")

            sleep(5)

            # select all checkboxes not already checked
            check_boxes = self.driver_session.find_elements(By.CSS_SELECTOR, '[type="checkbox"')
            for check_box in check_boxes:
                # lazy checks for checkboxes that may exist but shouldn't be clicked
                if (
                    check_box.get_attribute("name") == "DnDHours"
                    or check_box.get_attribute("name") == "checkboxLastRev"
                ):
                    continue  # don't click these

                # If not checked, check it
                is_checked = check_box.get_attribute("checked")
                if is_checked is None:
                    check_box.click()

            sleep(0.25)
            # # Ensure that all boxes are checked
            # for box in self.driver_session.find_elements(By.CSS_SELECTOR, '[type="checkbox"'):
            #     if (
            #         box.get_attribute("name") != "DnDHours"
            #         and box.get_attribute("name") != "checkboxLastRev"
            #         and box.get_attribute("checked") is None
            #     ):
            #         raise Exception("Not all boxes checked!")

            # Get all the buttons but only do stuff for ones that say "Download PDF File"
            for button in self.driver_session.find_elements(By.CSS_SELECTOR, ".ui-button-text"):
                if button.text == "Download PDF File":

                    # Clean up any existing files first before downloading
                    files = list(pathlib.Path(self.CHROME_DOWNLOAD_FOLDER_PATH).glob("**/*"))
                    for file in files:
                        os.remove(file)

                    button.click()
                    self._wait_for_chrome_downloads(number_of_files=1)

                    # Switch to the oppend "processing" tab, close it, and switch back
                    self.driver_session.switch_to.window(self.driver_session.window_handles[-1])
                    self.driver_session.close()
                    self.driver_session.switch_to.window(self.driver_session.window_handles[0])

                    # move to payload folder
                    files = os.listdir(self.CHROME_DOWNLOAD_FOLDER_PATH)[0]  # only expect one file
                    pathlib.Path(os.path.join(self.CHROME_DOWNLOAD_FOLDER_PATH, files)).replace(
                        os.path.join(
                            project_files_download_path,
                            re.sub(r".\d{6,8}\.\d{4}\.\d{2}\.pdf", ".pdf", str(files), count=0, flags=0),
                        )
                    )
                    break  # There is only one button that we click once, so break

        # if there is a next page, download that
        next_page = self.driver_session.find_elements(By.XPATH, "//*[@onmouseover]")
        for item in next_page:
            if item.accessible_name == "Go to next page":
                item.click()

                # recuse for each next page
                self._download_pdf_files(tab_name, sub_job_cost_doc_item)

                break  # probably don't need this but don't want to test it

    def _download_project_files(self, menu_name, sub_job_cost_doc_item):

        sleep(10)

        # get all the download links
        items_to_download = self.driver_session.find_elements(By.CSS_SELECTOR, '[onclick="down(this)"]')
        for item in items_to_download:
            down_url = item.get_attribute("data-url")

            # it's some weird half link windows path, that their backend handles
            # convert it to url path and add the rest of the url when downloading
            sanitized_down_url = str(down_url).replace("\\", "/")
            urlretrieve(
                url_quote(f"https://www.esubonline.com{sanitized_down_url}", safe="/:?&()"),
                os.path.join(
                    self.project_download_folder,
                    menu_name,
                    sub_job_cost_doc_item,
                    os.path.basename(sanitized_down_url),
                ),
            )

        # if there is a next page, download that
        next_page = self.driver_session.find_elements(By.XPATH, "//*[@onmouseover]")
        for item in next_page:
            if item.accessible_name == "Go to next page":
                item.click()

                # recuse for each next page
                self._download_project_files(menu_name, sub_job_cost_doc_item)

                break  # probably don't need this but don't want to test it

    # TODO:
    # This doesn't work, need to manually move the mouse to the middle
    # or find a way to programatically do it. for now we just use
    # self.project_urls that we gathered semi-manually
    def _scroll_down_page(self, speed=8):

        # Try #1
        total_height = int(self.driver_session.execute_script("return document.body.scrollHeight"))
        for i in range(1, total_height, 5):
            self.driver_session.execute_script(f"window.scrollTo(0, {i});")

        # Try #2
        y = 1000
        for timer in range(0, 50):
            self.driver_session.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += 1000
            sleep(1)

        # Try #3
        current_scroll_position, new_height = 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            self.driver_session.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = self.driver_session.execute_script("return document.body.scrollHeight")

        # Try #4
        scroll_window_location = self.driver_session.find_element(By.CSS_SELECTOR, ".infinite-scroll-container")
        action = ActionChains(self.driver_session)
        action.move_to_element_with_offset(scroll_window_location, 5, 5)
        action.perform()


def split_list(a, n):
    n = min(n, len(a))
    k, m = divmod(len(a), n)
    return list((a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)))


def download_files_single_thread():
    e = eSUB(None, download_proj=False)
    e.download_files()


if __name__ == "__main__":

    # download_files_single_thread()

    # TODO: Setup main window and get list of projects.
    # main_window = eSUB(None, download_proj=False)
    # project_urls = main_window.get_project_urls()

    working_url_list = unp.PROJECT_URLS

    # Setup main folder
    pathlib.Path(unp.DOWNLOAD_BASE_FOLDER).mkdir(parents=True, exist_ok=True)
    pathlib.Path(unp.REMAINING_PATH).mkdir(parents=True, exist_ok=True)
    pathlib.Path(unp.DEBUG_PATH).mkdir(parents=True, exist_ok=True)

    # See what still needs to be gotten if we are picking back up from a previous run
    remaining_urls = pathlib.Path(unp.REMAINING_PATH).glob("project_url_num_*")
    if len(list(remaining_urls)) > 0:
        working_url_list = remaining_urls

    # Create file for each url with name being f"project_url_num_{url_number}"
    for url_to_get in working_url_list:
        with open(os.path.join(unp.REMAINING_PATH, f"project_url_num_{os.path.basename(url_to_get)}"), "a") as fh:
            fh.write(url_to_get)

    i = 0
    while pathlib.Path(unp.REMAINING_PATH).glob("project_url_num_*") and i < 10:
        remaining_urls = pathlib.Path(unp.REMAINING_PATH).glob("project_url_num_*")

        working_url_list = []
        for url_path in remaining_urls:
            working_url_list.append(f"https://app.esub.com/project/{str(url_path).split('_')[-1]}")

        random.shuffle(working_url_list)

        with Pool(cpu_count()) as p:
            # p.map(eSUB, working_url_list)
            for _ in tqdm(p.imap_unordered(eSUB, working_url_list), total=len(working_url_list)):
                pass

        i += 1
