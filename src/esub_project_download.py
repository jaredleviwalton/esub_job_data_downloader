import os
import re
import json
import pathlib
from time import sleep
from urllib.request import urlretrieve
from urllib.parse import quote as url_quote

from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import users_and_passwords as unp


class eSUB:
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
        "https://app.esub.com/project/10145",
        "https://app.esub.com/project/10144",
        "https://app.esub.com/project/10184",
        "https://app.esub.com/project/10186",
        "https://app.esub.com/project/10192",
        "https://app.esub.com/project/10209",
        "https://app.esub.com/project/10210",
        "https://app.esub.com/project/10222",
        "https://app.esub.com/project/10096",
        "https://app.esub.com/project/48",
        "https://app.esub.com/project/26",
        "https://app.esub.com/project/10061",
        "https://app.esub.com/project/10153",
        "https://app.esub.com/project/10156",
        "https://app.esub.com/project/10160",
        "https://app.esub.com/project/10169",
        "https://app.esub.com/project/10182",
        "https://app.esub.com/project/10235",
        "https://app.esub.com/project/10236",
        "https://app.esub.com/project/10134",
        "https://app.esub.com/project/10143",
        "https://app.esub.com/project/10149",
        "https://app.esub.com/project/10158",
        "https://app.esub.com/project/10172",
        "https://app.esub.com/project/10175",
        "https://app.esub.com/project/10185",
        "https://app.esub.com/project/10193",
        "https://app.esub.com/project/13",
        "https://app.esub.com/project/27",
        "https://app.esub.com/project/10065",
        "https://app.esub.com/project/10062",
        "https://app.esub.com/project/10064",
        "https://app.esub.com/project/10066",
        "https://app.esub.com/project/10068",
        "https://app.esub.com/project/10085",
        "https://app.esub.com/project/10081",
        "https://app.esub.com/project/10107",
        "https://app.esub.com/project/10212",
        "https://app.esub.com/project/10121",
        "https://app.esub.com/project/10132",
        "https://app.esub.com/project/10191",
        "https://app.esub.com/project/42",
        "https://app.esub.com/project/10106",
        "https://app.esub.com/project/10128",
        "https://app.esub.com/project/10137",
        "https://app.esub.com/project/10151",
        "https://app.esub.com/project/10155",
        "https://app.esub.com/project/10159",
        "https://app.esub.com/project/10164",
        "https://app.esub.com/project/10181",
        "https://app.esub.com/project/10188",
        "https://app.esub.com/project/10221",
        "https://app.esub.com/project/10229",
        "https://app.esub.com/project/30",
        "https://app.esub.com/project/10224",
        "https://app.esub.com/project/10248",
        "https://app.esub.com/project/10180",
        "https://app.esub.com/project/10201",
        "https://app.esub.com/project/10086",
        "https://app.esub.com/project/10101",
        "https://app.esub.com/project/21",
        "https://app.esub.com/project/24",
        "https://app.esub.com/project/17",
        "https://app.esub.com/project/7",
        "https://app.esub.com/project/11",
        "https://app.esub.com/project/43",
        "https://app.esub.com/project/10069",
        "https://app.esub.com/project/10094",
        "https://app.esub.com/project/10166",
        "https://app.esub.com/project/10171",
        "https://app.esub.com/project/10194",
        "https://app.esub.com/project/10233",
        "https://app.esub.com/project/10238",
        "https://app.esub.com/project/10078",
        "https://app.esub.com/project/20",
        "https://app.esub.com/project/10058",
        "https://app.esub.com/project/3",
        "https://app.esub.com/project/29",
        "https://app.esub.com/project/53",
        "https://app.esub.com/project/10073",
        "https://app.esub.com/project/10095",
        "https://app.esub.com/project/10148",
        "https://app.esub.com/project/10141",
        "https://app.esub.com/project/10199",
        "https://app.esub.com/project/10211",
        "https://app.esub.com/project/10074",
        "https://app.esub.com/project/10093",
        "https://app.esub.com/project/10219",
        "https://app.esub.com/project/10079",
        "https://app.esub.com/project/10126",
        "https://app.esub.com/project/10071",
        "https://app.esub.com/project/10208",
        "https://app.esub.com/project/10080",
        "https://app.esub.com/project/10088",
        "https://app.esub.com/project/10187",
        "https://app.esub.com/project/10227",
        "https://app.esub.com/project/10117",
        "https://app.esub.com/project/10119",
        "https://app.esub.com/project/10130",
        "https://app.esub.com/project/49",
        "https://app.esub.com/project/10112",
        "https://app.esub.com/project/10138",
        "https://app.esub.com/project/33",
        "https://app.esub.com/project/10076",
        "https://app.esub.com/project/10207",
        "https://app.esub.com/project/10214",
        "https://app.esub.com/project/10114",
        "https://app.esub.com/project/10075",
        "https://app.esub.com/project/10237",
        "https://app.esub.com/project/10120",
        "https://app.esub.com/project/12",
        "https://app.esub.com/project/36",
        "https://app.esub.com/project/35",
        "https://app.esub.com/project/10057",
        "https://app.esub.com/project/10056",
        "https://app.esub.com/project/10067",
        "https://app.esub.com/project/10070",
        "https://app.esub.com/project/10077",
        "https://app.esub.com/project/10083",
        "https://app.esub.com/project/10113",
        "https://app.esub.com/project/10127",
        "https://app.esub.com/project/10136",
        "https://app.esub.com/project/10147",
        "https://app.esub.com/project/10142",
        "https://app.esub.com/project/10161",
        "https://app.esub.com/project/10154",
        "https://app.esub.com/project/10163",
        "https://app.esub.com/project/10165",
        "https://app.esub.com/project/10168",
        "https://app.esub.com/project/10170",
        "https://app.esub.com/project/10178",
        "https://app.esub.com/project/10179",
        "https://app.esub.com/project/10198",
        "https://app.esub.com/project/10234",
        "https://app.esub.com/project/10244",
        "https://app.esub.com/project/10245",
        "https://app.esub.com/project/10246",
        "https://app.esub.com/project/10082",
        "https://app.esub.com/project/10150",
        "https://app.esub.com/project/10087",
        "https://app.esub.com/project/10157",
        "https://app.esub.com/project/10167",
        "https://app.esub.com/project/10177",
        "https://app.esub.com/project/10102",
        "https://app.esub.com/project/9",
        "https://app.esub.com/project/45",
        "https://app.esub.com/project/8",
        "https://app.esub.com/project/51",
        "https://app.esub.com/project/10092",
        "https://app.esub.com/project/10131",
        "https://app.esub.com/project/10203",
        "https://app.esub.com/project/10176",
        "https://app.esub.com/project/50",
        "https://app.esub.com/project/56",
        "https://app.esub.com/project/10216",
        "https://app.esub.com/project/40",
        "https://app.esub.com/project/10116",
        "https://app.esub.com/project/19",
        "https://app.esub.com/project/28",
        "https://app.esub.com/project/10189",
        "https://app.esub.com/project/5",
        "https://app.esub.com/project/54",
        "https://app.esub.com/project/16",
        "https://app.esub.com/project/10110",
        "https://app.esub.com/project/14",
        "https://app.esub.com/project/10223",
        "https://app.esub.com/project/23",
        "https://app.esub.com/project/25",
        "https://app.esub.com/project/15",
        "https://app.esub.com/project/47",
        "https://app.esub.com/project/55",
        "https://app.esub.com/project/10118",
        "https://app.esub.com/project/10202",
        "https://app.esub.com/project/10204",
        "https://app.esub.com/project/10105",
        "https://app.esub.com/project/22",
        "https://app.esub.com/project/52",
        "https://app.esub.com/project/10108",
        "https://app.esub.com/project/10174",
        "https://app.esub.com/project/18",
        "https://app.esub.com/project/4",
        "https://app.esub.com/project/6",
        "https://app.esub.com/project/10",
        "https://app.esub.com/project/31",
        "https://app.esub.com/project/10152",
        "https://app.esub.com/project/37",
        "https://app.esub.com/project/38",
        "https://app.esub.com/project/10060",
        "https://app.esub.com/project/32",
        "https://app.esub.com/project/34",
        "https://app.esub.com/project/41",
        "https://app.esub.com/project/10183",
        "https://app.esub.com/project/10195",
        "https://app.esub.com/project/39",
        "https://app.esub.com/project/10196",
        "https://app.esub.com/project/10226",
        "https://app.esub.com/project/10230",
        "https://app.esub.com/project/46",
        "https://app.esub.com/project/10063",
        "https://app.esub.com/project/10084",
        "https://app.esub.com/project/10097",
        "https://app.esub.com/project/10111",
        "https://app.esub.com/project/10059",
        "https://app.esub.com/project/10089",
        "https://app.esub.com/project/10099",
        "https://app.esub.com/project/10090",
        "https://app.esub.com/project/10091",
        "https://app.esub.com/project/10228",
        "https://app.esub.com/project/10109",
        "https://app.esub.com/project/10146",
        "https://app.esub.com/project/10217",
        "https://app.esub.com/project/10253",
        "https://app.esub.com/project/10254",
        "https://app.esub.com/project/10255",
        "https://app.esub.com/project/10260",
        "https://app.esub.com/project/10256",
        "https://app.esub.com/project/10258",
        "https://app.esub.com/project/10259",
        "https://app.esub.com/project/10261",
        "https://app.esub.com/project/10262",
        "https://app.esub.com/project/10263",
        "https://app.esub.com/project/10264",
        "https://app.esub.com/project/10265",
        "https://app.esub.com/project/10266",
        "https://app.esub.com/project/10267",
        "https://app.esub.com/project/10271",
        "https://app.esub.com/project/10268",
        "https://app.esub.com/project/10269",
        "https://app.esub.com/project/10270",
        "https://app.esub.com/project/10272",
        "https://app.esub.com/project/10275",
        "https://app.esub.com/project/10273",
        "https://app.esub.com/project/10274",
        "https://app.esub.com/project/10276",
        "https://app.esub.com/project/10277",
        "https://app.esub.com/project/10278",
        "https://app.esub.com/project/10280",
        "https://app.esub.com/project/10281",
        "https://app.esub.com/project/10279",
        "https://app.esub.com/project/10282",
        "https://app.esub.com/project/10289",
        "https://app.esub.com/project/10283",
        "https://app.esub.com/project/10284",
        "https://app.esub.com/project/10285",
        "https://app.esub.com/project/10286",
        "https://app.esub.com/project/10287",
        "https://app.esub.com/project/10288",
        "https://app.esub.com/project/10291",
        "https://app.esub.com/project/10290",
        "https://app.esub.com/project/10247",
        "https://app.esub.com/project/10139",
        "https://app.esub.com/project/10173",
        "https://app.esub.com/project/10197",
        "https://app.esub.com/project/10162",
        "https://app.esub.com/project/10190",
        "https://app.esub.com/project/10200",
        "https://app.esub.com/project/10250",
        "https://app.esub.com/project/10251",
        "https://app.esub.com/project/10205",
        "https://app.esub.com/project/10213",
        "https://app.esub.com/project/10220",
        "https://app.esub.com/project/10218",
        "https://app.esub.com/project/10241",
        "https://app.esub.com/project/10225",
        "https://app.esub.com/project/10239",
        "https://app.esub.com/project/10231",
        "https://app.esub.com/project/10232",
        "https://app.esub.com/project/10240",
        "https://app.esub.com/project/10242",
        "https://app.esub.com/project/10243",
        "https://app.esub.com/project/10249",
        "https://app.esub.com/project/10252",
        "https://app.esub.com/project/10122",
        "https://app.esub.com/project/10098",
        "https://app.esub.com/project/10129",
        "https://app.esub.com/project/44",
        "https://app.esub.com/project/10123",
        "https://app.esub.com/project/10206",
        "https://app.esub.com/project/10125",
        "https://app.esub.com/project/10124",
    ]

    LOGIN_URL = "https://app.esub.com/login"
    PROJECTS_URL = "https://app.esub.com/project"

    CHROME_DOWNLOAD_FOLDER_PATH = r"C:\Users\jawalking\tmp"

    DOWNLOAD_BASE_FOLDER = r"C:\Users\jawalking\new_payload"

    # existing driver session for debugging and when it breaks
    # update as needed
    EXISTING_SESSION_URL = "http://localhost:55185"
    EXISTING_SESSION_ID = "a43ba8c76f344a3f064797247aa41ae4"

    def __init__(self, use_existing_session=False) -> None:
        if use_existing_session:
            self.driver_session = webdriver.Remote(command_executor=self.EXISTING_SESSION_URL, desired_capabilities={})
            self.driver_session.close()
            self.driver_session.session_id = self.EXISTING_SESSION_ID
        else:
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
                "download.default_directory": self.CHROME_DOWNLOAD_FOLDER_PATH,  # our temp download location
                "download.prompt_for_download": False,  # for saving pdf files
                "download.directory_upgrade": True,  # for saving pdf files
                "plugins.always_open_pdf_externally": True,  # Don't open PDF in chrome
                "printing.print_preview_sticky_settings.appState": json.dumps(settings),  # for pdf printing
                "savefile.default_directory": self.CHROME_DOWNLOAD_FOLDER_PATH,  # for pdf printing
            }
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--kiosk-printing")  # for pdf printing
            self.driver_session = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
            print(f"{self.driver_session.command_executor._url=}")  # We'll need this for keeping this session
            print(f"{self.driver_session.session_id=}")  # We'll need this for keeping this session
            self._login()

    def _login(self) -> None:
        self.driver_session.get(self.LOGIN_URL)

        self._wait_for(element_id="txtUsername")

        self.driver_session.find_element_by_id("txtUsername").send_keys(unp.USER_NAME)
        self.driver_session.find_element_by_id("txtPassword").send_keys(unp.USER_PASS)

        self.driver_session.find_element_by_id("btnLogin").click()

        sleep(5)

    # Use self.project_urls instead
    def _get_projects(self):
        self.driver_session.get(self.PROJECTS_URL)
        self._wait_for(css_selector=".project-card")

        # scroll down the page to force all projects to populate
        # TODO: this has problems, need to manually scroll or move mouse to middle
        self._scroll_down_page()

        # get projects list and keep it
        self.projects = self.driver_session.find_elements_by_css_selector(".project-card")

        for project in self.projects:
            project_url = project.get_attribute("href")
            print(project_url)

    def _get_windows_path_safe_string(self, string) -> str:
        return re.sub(r'[\\/\:*"<>\|\.%\$\^]', "", string)

    def download_files(self) -> None:

        for project_url in tqdm(self.PROJECT_URLS):
            print("\n")

            # Load the project page
            self.driver_session.get(project_url)

            # get the url id number to help with non-unique names
            url_id = os.path.basename(project_url)

            # get the project name
            self._wait_for(class_name="es-project-summary__title")
            project_name = (
                str(self.driver_session.find_elements_by_class_name("es-project-summary__title")[0].text)
                .strip(r"business")
                .strip(r"keybaord_arrow_down")
                .strip("\n")
            )

            # windows path safe project name
            project_name = self._get_windows_path_safe_string(project_name)

            # the project download folder is the url id + the project name
            project_download_folder = os.path.join(self.DOWNLOAD_BASE_FOLDER, f"{url_id} - {project_name}")
            print(project_download_folder)
            pathlib.Path(project_download_folder).mkdir(parents=True, exist_ok=True)

            # required items to get
            self._get_files(project_download_folder, "Project Files")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_files(project_download_folder, "Company Files")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Job Cost Docs", "Change Order Requests")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Construction Docs", "Requests For Information")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Construction Docs", "Submittals")

            # Extras
            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Job Cost Docs", "Purchase Orders")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Job Cost Docs", "Subcontracts")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Job Cost Docs", "Subcontract Change Orders")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Job Cost Docs", "Pay Applications")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Construction Docs", "Field Notes")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Construction Docs", "Meeting Minutes")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Construction Docs", "Equipment Rental")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Construction Docs", "Correspondence Log")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Project", "Issues")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Construction Docs", "Daily Reports")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Construction Docs", "Drawing Sets")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_emails(project_download_folder, "Project", "Project Inbox")

            self.driver_session.get(project_url)
            # sleep(3)
            self._wait_for(class_name="es-project-summary__title")
            self._get_typical_page_docs(project_download_folder, "Project", "Contacts", download_files=False)

    def _get_files(self, project_download_folder, sub_job_cost_doc_item):
        # get the files dropdown and click on it
        for dropdown in self.driver_session.find_elements_by_css_selector(".es-dropdown-menu-trigger"):
            if "Files" == dropdown.text:
                dropdown.click()

                sleep(1)

                # get the projects files sub menu item and click on it
                for item in self.driver_session.find_elements_by_css_selector(".es-dropdown-menu__item"):
                    if sub_job_cost_doc_item == item.text:
                        item.click()
                        break

                pathlib.Path(os.path.join(project_download_folder, "Files", sub_job_cost_doc_item)).mkdir(
                    parents=True, exist_ok=True
                )

                self._download_project_files(project_download_folder, sub_job_cost_doc_item)

    def _get_emails(self, project_download_folder, tab_name, sub_job_cost_doc_item):
        # get the files dropdown and click on it
        menus = self.driver_session.find_elements_by_css_selector(".es-dropdown-menu-trigger")
        for dropdown in menus:
            if tab_name in str(dropdown.accessible_name):
                dropdown.click()

                sleep(2)

                # get the projects files sub menu item and click on it
                sub_menus = self.driver_session.find_elements_by_css_selector(".es-dropdown-menu__item")
                for item in sub_menus:
                    if sub_job_cost_doc_item in item.text:
                        item.click()
                        break

                # sleep(5)
                self._wait_for(
                    css_selector="[onmouseover=\"window.status='Go to eSUB Inc. corporate site';return true;\"]"
                )
                pathlib.Path(os.path.join(project_download_folder, tab_name)).mkdir(parents=True, exist_ok=True)

                # get excel summary
                on_mouse_over_items = self.driver_session.find_elements_by_xpath('//*[@name="IconXLS1"]')
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
                            os.path.join(project_download_folder, tab_name, f"{sub_job_cost_doc_item}.xls")
                        )
                        # sleep(2)
                        break

                # download files
                self._save_email(project_download_folder, tab_name, sub_job_cost_doc_item)

                break

    def _get_typical_page_docs(self, project_download_folder, menu_name, sub_menu_name, download_files=True):
        # get the files dropdown and click on it
        menus = self.driver_session.find_elements_by_css_selector(".es-dropdown-menu-trigger")
        for dropdown in menus:
            if menu_name in str(dropdown.accessible_name):
                dropdown.click()

                sleep(2)

                # get the projects files sub menu item and click on it
                sub_menus = self.driver_session.find_elements_by_css_selector(".es-dropdown-menu__item")
                for item in sub_menus:
                    if sub_menu_name in item.text:
                        item.click()
                        break

                # sleep(4)
                self._wait_for(
                    css_selector="[onmouseover=\"window.status='Go to eSUB Inc. corporate site';return true;\"]"
                )
                pathlib.Path(os.path.join(project_download_folder, menu_name)).mkdir(parents=True, exist_ok=True)

                # get excel summary
                on_mouse_over_items = self.driver_session.find_elements_by_xpath('//*[@name="IconXLS1"]')
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
                            os.path.join(project_download_folder, menu_name, f"{sub_menu_name}.xls")
                        )

                        break  # We are done here, don't try to process inactive menu items

                if download_files:
                    self._download_pdf_files(project_download_folder, menu_name, sub_menu_name)

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

    def _save_email(self, project_download_folder, tab_name, sub_job_cost_doc_item):

        # Setup project email download path
        download_path = os.path.join(project_download_folder, tab_name, sub_job_cost_doc_item)
        pathlib.Path(download_path).mkdir(parents=True, exist_ok=True)

        items_to_download = self.driver_session.find_elements_by_css_selector(
            '[alt="View this Incoming Correspondence"]'
        )
        email_numbers = self.driver_session.find_elements_by_css_selector('[alt="Created from Incoming Email"]')

        # For some reason getting these items in reverse order causes hangs...
        # for item, number_element in zip(items_to_download[::-1], email_numbers[::-1]):
        for item, number_element in zip(items_to_download, email_numbers):
            email_number = number_element.find_element_by_xpath("../..").text

            item.click()
            sleep(3)

            # Clean up any existing files first before downloading
            files = list(pathlib.Path(self.CHROME_DOWNLOAD_FOLDER_PATH).glob("**/*"))
            for file in files:
                os.remove(file)

            # Switch to just oppend tab
            self.driver_session.switch_to.window(self.driver_session.window_handles[-1])

            # The name is the only element with this bg class on the page
            email_name = e.driver_session.find_elements_by_xpath('//*[@class="bgcolor3"]')[0].accessible_name
            email_name = self._get_windows_path_safe_string(email_name)

            # Print email and move to project email folder
            e.driver_session.execute_script("window.print();")
            files = os.listdir(self.CHROME_DOWNLOAD_FOLDER_PATH)[0]  # only one file expected
            pathlib.Path(os.path.join(self.CHROME_DOWNLOAD_FOLDER_PATH, files)).replace(
                os.path.join(download_path, f"{email_number} - {email_name}.pdf")
            )

            # Attachment links are next to these icons, so get all of them
            attachment_icon_elements = self.driver_session.find_elements_by_css_selector(
                '[src="/TRACKpoint/images/icons/attachment.png"]'
            )
            for attachment_icon_element in attachment_icon_elements:

                # get the parent and sibling element(s) for the attachment icon
                # sibling at index 0 is the icon
                # sibling at index 1 is the attachment name
                # sibling at index 2 is the download link
                parent_element = attachment_icon_element.find_element_by_xpath("../..")
                sibling_elements = parent_element.find_elements_by_xpath("*")

                attachment_name = sibling_elements[1].text
                attachment_name = self._get_windows_path_safe_string(attachment_name)

                down_url = sibling_elements[2].find_elements_by_xpath("*")[0].get_attribute("href")

                save_path = os.path.join(
                    download_path, f"{email_number} - {email_name} - Attachment - {attachment_name}"
                )

                if os.path.exists(save_path):
                    # hacky check for duplicate email attachment
                    # if broken here write increment logic
                    raise Exception(" duplicate email attachment, write increment logic!")

                # Download attachment
                urlretrieve(url_quote(down_url, safe="/:?&()"), save_path)

            # Close Tab and switch context to main tab
            self.driver_session.close()
            self.driver_session.switch_to.window(self.driver_session.window_handles[0])

        # if there is a next page, download that
        next_page = e.driver_session.find_elements_by_xpath("//*[@onmouseover]")
        for item in next_page:
            if item.accessible_name == "Go to next page":
                item.click()

                # recuse for each next page
                self._save_email(project_download_folder, tab_name, sub_job_cost_doc_item)

                break  # probably don't need this but don't want to test it

    def _download_pdf_files(self, project_download_folder, tab_name, sub_job_cost_doc_item):

        self._wait_for(css_selector="[onmouseover=\"window.status='Go to eSUB Inc. corporate site';return true;\"]")

        project_files_download_path = os.path.join(project_download_folder, tab_name, sub_job_cost_doc_item)
        pathlib.Path(project_files_download_path).mkdir(parents=True, exist_ok=True)

        # Get all the download as PDF items
        items_to_download = self.driver_session.find_elements_by_css_selector('[alt="Download as PDF"]')

        # For some reason this wants things from the bottom up, or it hangs.
        for item in items_to_download[::-1]:
            item.click()
            sleep(3)

            # select all checkboxes not already checked
            check_boxes = self.driver_session.find_elements_by_css_selector('[type="checkbox"')
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

            # Get all the buttons but only do stuff for ones that say "Download PDF File"
            for button in self.driver_session.find_elements_by_css_selector(".ui-button-text"):
                if button.text == "Download PDF File":

                    # Clean up any existing files first before downloading
                    files = list(pathlib.Path(self.CHROME_DOWNLOAD_FOLDER_PATH).glob("**/*"))
                    for file in files:
                        os.remove(file)

                    sleep(0.5)  # wait half a beat after checking boxes
                    button.click()
                    self._wait_for_chrome_downloads(number_of_files=1)

                    # Switch to the oppend "processing" tab, close it, and switch back
                    self.driver_session.switch_to.window(self.driver_session.window_handles[-1])
                    self.driver_session.close()
                    self.driver_session.switch_to.window(self.driver_session.window_handles[0])

                    # move to payload folder
                    files = os.listdir(self.CHROME_DOWNLOAD_FOLDER_PATH)
                    pathlib.Path(os.path.join(self.CHROME_DOWNLOAD_FOLDER_PATH, files[0])).replace(
                        os.path.join(
                            project_files_download_path,
                            re.sub(r".\d{8}\.\d{4}\.\d{2}\.pdf", ".pdf", str(files[0]), count=0, flags=0),
                        )
                    )
                    break  # There is only one button that we click once, so break

        # if there is a next page, download that
        next_page = e.driver_session.find_elements_by_xpath("//*[@onmouseover]")
        for item in next_page:
            if item.accessible_name == "Go to next page":
                item.click()

                # recuse for each next page
                self._download_pdf_files(project_download_folder, tab_name, sub_job_cost_doc_item)

                break  # probably don't need this but don't want to test it

    def _download_project_files(self, project_download_folder, sub_job_cost_doc_item):

        self._wait_for(css_selector="[onmouseover=\"window.status='Go to eSUB Inc. corporate site';return true;\"]")

        # get all the download links
        items_to_download = e.driver_session.find_elements_by_css_selector('[onclick="down(this)"]')
        for item in items_to_download:
            down_url = item.get_attribute("data-url")

            # it's some weird half link windows path, that their backend handles
            # convert it to url path and add the rest of the url when downloading
            sanitized_down_url = str(down_url).replace("\\", "/")
            urlretrieve(
                url_quote(f"https://www.esubonline.com{sanitized_down_url}", safe="/:?&()"),
                os.path.join(
                    project_download_folder, "Files", sub_job_cost_doc_item, os.path.basename(sanitized_down_url)
                ),
            )

        # if there is a next page, download that
        next_page = e.driver_session.find_elements_by_xpath("//*[@onmouseover]")
        for item in next_page:
            if item.accessible_name == "Go to next page":
                item.click()

                # recuse for each next page
                self._download_project_files(project_download_folder, sub_job_cost_doc_item)

                break  # probably don't need this but don't want to test it

    # "Fancy" wait that I never had time or care to use except for login
    def _wait_for(self, element_id=None, element_name=None, css_selector=None, class_name=None, timeout=300):

        sleep(1)

        if element_id is not None and element_name is None and css_selector is None and class_name is None:
            WebDriverWait(driver=self.driver_session, timeout=timeout).until(
                lambda x: x.find_element_by_id(element_id).is_displayed()
            )
        elif element_name is not None and element_id is None and css_selector is None and class_name is None:
            WebDriverWait(driver=self.driver_session, timeout=timeout).until(
                lambda x: x.find_element_by_name(element_name).is_displayed()
            )
        elif css_selector is not None and element_id is None and element_name is None and class_name is None:
            WebDriverWait(driver=self.driver_session, timeout=timeout).until(
                lambda x: len(x.find_elements_by_css_selector(css_selector)) > 0
            )
        elif class_name is not None and element_id is None and element_name is None and css_selector is None:
            WebDriverWait(driver=self.driver_session, timeout=timeout).until(
                lambda x: len(x.find_elements_by_class_name(class_name))
            )
        else:
            raise ValueError("Bad _wait_for combo", element_id, element_name, timeout)

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
        scroll_window_location = self.driver_session.find_element_by_css_selector(".infinite-scroll-container")
        action = webdriver.common.action_chains.ActionChains(self.driver_session)
        action.move_to_element_with_offset(scroll_window_location, 5, 5)
        action.perform()


if __name__ == "__main__":
    e = eSUB()
    e.download_files()
