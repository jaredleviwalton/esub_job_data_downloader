from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import users_and_passwords as unp


class eSUB:
    LOGIN_URL = "https://app.esub.com/login"
    PROJECTS_URL = "https://app.esub.com/project"

    def __init__(self) -> None:
        self.driver_session = webdriver.Chrome("chromedriver")

        self._login()

    def _login(self) -> None:
        self.driver_session.get(self.LOGIN_URL)

        self._wait_for(element_id="txtUsername")

        self.driver_session.find_element_by_id("txtUsername").send_keys(unp.USER_NAME)
        self.driver_session.find_element_by_id("txtPassword").send_keys(unp.USER_PASS)

        self.driver_session.find_element_by_id("btnLogin").click()

    def download_files(self) -> None:

        self.driver_session.get(self.PROJECTS_URL)
        self._wait_for(css_selector=".project-card")

        # scroll down the page to force all projects to populate
        self._scroll_down_page()

        # get projects list and keep it
        self.projects = self.driver_session.find_elements_by_css_selector('.project-card')

        for project in self.projects:
            project.click()
            sleep(5)

            # get the files dropdown and click on it
            for dropdown in self.driver_session.find_elements_by_css_selector('.es-dropdown-menu-trigger'):
                if 'Files' == dropdown.text:
                    dropdown.click()
                    sleep(5)

                    # get the projects files sub menu item and click on it
                    for item in self.driver_session.find_elements_by_css_selector('.es-dropdown-menu__item'):
                        if 'Project Files' == item.text:
                            item.click()
                            sleep(5)

                            # find the table and download the attatchents
                            my_table = self.driver_session.find_element_by_css_selector('table.outputtbl')

                            # if the first cell in the row has a download link click it
                            for row in my_table.find_elements_by_css_selector('tr'):
                                for cell in row.find_elements_by_tag_name('td'):
                                    print(cell.text)

                            # Check if there are more tables to download from... probably want to create a function for the above

            # go back to projects page
            self.driver_session.get(self.PROJECTS_URL)
            sleep(20)

    def _wait_for(self, element_id=None, element_name=None, css_selector=None, timeout=20):

        sleep(5)

        if element_id is not None and element_name is None and css_selector is None:
            WebDriverWait(driver=self.driver_session, timeout=timeout).until(
                lambda x: x.find_element_by_id(element_id).is_displayed()
            )
        elif element_name is not None and element_id is None and css_selector is None:
            WebDriverWait(driver=self.driver_session, timeout=timeout).until(
                lambda x: x.find_element_by_name(element_name).is_displayed()
            )
        elif css_selector is not None and element_id is None and element_name is None:
            WebDriverWait(driver=self.driver_session, timeout=timeout).until(lambda x: len(x.find_elements_by_css_selector(css_selector)) > 0)
        else:
            raise ValueError("Bad _wait_for combo", element_id, element_name, timeout)

    def _scroll_down_page(self, speed=8):
        # Try #1
        total_height = int(self.driver_session.execute_script("return document.body.scrollHeight"))

        for i in range(1, total_height, 5):
            self.driver_session.execute_script("window.scrollTo(0, {});".format(i))

        # Try #2
        # y = 1000
        # for timer in range(0,50):
        #     self.driver_session.execute_script("window.scrollTo(0, "+str(y)+")")
        #     y += 1000
        #     sleep(1)

        # Try #3
        # current_scroll_position, new_height= 0, 1
        # while current_scroll_position <= new_height:
        #     current_scroll_position += speed
        #     self.driver_session.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        #     new_height = self.driver_session.execute_script("return document.body.scrollHeight")


if __name__ == "__main__":
    e = eSUB()
    e.download_files()
