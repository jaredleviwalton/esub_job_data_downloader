import logging as log
import os
import pathlib
import traceback
from typing import List

import pandas as pd
import win32com.client

import users_and_passwords as unp


log.basicConfig(
    level=log.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    handlers=[
        log.FileHandler(filename=os.path.join(unp.BASE_FOLDER, "validation.log"), mode="a"),
        log.StreamHandler(),
    ],
)


class ValidateESUB:
    def convert_broken_xls_to_working_xlsx(self, xls_path: str) -> bool:
        if not os.path.exists(xls_path):
            log.warning(f"File does not exist; {xls_path=}")
            return False

        xls_path = pathlib.Path(xls_path)

        if xls_path.suffix != ".xls":
            log.error(f"File has extension '{xls_path.suffix}' not xls; {xls_path=}")
            return False

        xlsx_path = pathlib.Path(str(xls_path)[:-3] + "xlsx")

        try:
            # Get handle to excel
            excel_handle = win32com.client.Dispatch("Excel.Application")
            excel_handle.Visible = True

            # Open the file and and save as xlsx
            open_excel_file = excel_handle.Workbooks.Open(str(xls_path))
            open_excel_file.ActiveSheet.SaveAs(xlsx_path, 51)  # 51 is for xlsx
            open_excel_file.Close(SaveChanges=True)

            # Cleanup
            excel_handle.Quit()
            os.remove(xls_path)
        except:
            log.error(f"Error converting file; {xls_path=}")
            log.error(traceback.format_exc())
            return False
        else:
            return True

    def _check_xls_exists(self, file_path: str) -> None:
        xls_path = file_path
        xlsx_path = xls_path + "x"

        if not os.path.exists(xls_path) and not os.path.exists(xlsx_path):
            log.fatal(f"Excel file missing: {xls_path=}")
            return False
        else:
            return True

    def _check_convert_xls_to_xlsx(self, file_path: str) -> None:
        if not os.path.exists(file_path + "x"):
            self.convert_broken_xls_to_working_xlsx(file_path)
        else:
            return True

    def _check_files(
        self,
        files_folder_path: str,
        df: pd.DataFrame,
        start_listening_text: str,
        text_column_num: int,
        skip_text: List[str] | None,
        is_email: bool,
    ) -> None:
        file_nums_to_check = []
        listening = False

        # df row counter
        i = 0

        # skip until we find the start watching text
        while i < len(df):
            this_rows_column_zero_contents = str(df.iloc[i][0]).strip()
            if this_rows_column_zero_contents == start_listening_text:
                i += 1
                break
            i += 1

        # Get item numbers, ignoring blanks
        len_df = len(df)
        while i < len(df):
            this_rows_column_zero_contents = str(df.iloc[i][text_column_num]).strip()
            if this_rows_column_zero_contents != "nan" and this_rows_column_zero_contents not in skip_text:
                file_nums_to_check.append(str(this_rows_column_zero_contents).replace(" ", "-"))
            i += 1

        # for each item number, check for a corresponding file
        for file_num in file_nums_to_check:
            if not is_email:
                file_paths = list(pathlib.Path(files_folder_path).glob(f"*-{file_num}.pdf"))
                if len(list(file_paths)) == 0:
                    if file_num.isdecimal():
                        file_paths += list(pathlib.Path(files_folder_path).glob(f"*-{int(file_num):02d}.pdf"))
                        file_paths += list(pathlib.Path(files_folder_path).glob(f"*-{int(file_num):03d}.pdf"))
                    else:
                        pass
            else:
                file_paths = list(pathlib.Path(files_folder_path).glob(f"{file_num} - *.pdf"))
                new_file_paths = []
                for i, file_path in enumerate(file_paths):
                    if " - Attachment - " not in file_path.name:
                        new_file_paths.append(file_path)
                file_paths = new_file_paths

        if is_email:
            num_files_expected = len(file_nums_to_check)
            file_paths = list(pathlib.Path(files_folder_path).glob(f"*"))
            new_file_paths = []
            for i, file_path in enumerate(file_paths):
                if " - Attachment - " not in file_path.name:
                    new_file_paths.append(file_path)
            file_paths = new_file_paths
            num_files_found = len(file_paths)
            if num_files_found != num_files_expected:
                log.critical(f'"{files_folder_path}":\t{num_files_found=} != {num_files_expected=}')

        # Verify num expected with num present
        if not is_email:
            num_files_found = len(list(pathlib.Path(files_folder_path).glob("*")))
            num_files_expected = len(file_nums_to_check)
            if num_files_found != num_files_expected:
                log.critical(f'"{files_folder_path}":\t{num_files_found=} != {num_files_expected=}')

    def _validate(
        self,
        has_files: bool,
        files_folder_path: str,
        start_listening_text: str,
        text_column_num: int = 0,
        skip_text: List[str] = [],
        is_email: bool = False,
    ) -> bool:

        xls_path = files_folder_path + ".xls"
        xlsx_path = xls_path + "x"

        if self._check_xls_exists(xls_path):
            if self._check_convert_xls_to_xlsx(xls_path):
                df = pd.read_excel(xlsx_path, engine="openpyxl")

                if len(df.index) == 0 and len(df.columns) == 0:
                    log.debug(f"No items in: {xlsx_path}")
                    return True

                if has_files:
                    return self._check_files(
                        files_folder_path, df, start_listening_text, text_column_num, skip_text, is_email
                    )

        return False


class ValidateConstructionDocs(ValidateESUB):
    tab_name = "Construction Docs"

    def __init__(self, project_folder_path) -> None:
        self.project_folder_path = project_folder_path

        self.validate_correspondence_log()
        self.validate_daily_reports()
        self.validate_drawing_sets()
        self.validate_equipment_rental()
        self.validate_meeting_minutes()
        self.validate_requests_for_information()
        self.validate_submittals()

    def validate_correspondence_log(self):
        sub_tab_name = "Correspondence Log"
        has_files = True
        start_listening_text = "Number"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)

    def validate_daily_reports(self):
        sub_tab_name = "Daily Reports"
        has_files = True
        start_listening_text = "DR No"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)

    def validate_drawing_sets(self):
        sub_tab_name = "Drawing Sets"
        has_files = True
        start_listening_text = "Drawing Set Prefix"
        text_column_num = 1
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text, text_column_num)

    def validate_equipment_rental(self):
        sub_tab_name = "Equipment Rental"
        has_files = True
        start_listening_text = "No"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)

    def validate_meeting_minutes(self):
        sub_tab_name = "Meeting Minutes"
        has_files = True
        start_listening_text = "No"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)

    def validate_requests_for_information(self):
        sub_tab_name = "Requests For Information"
        has_files = True
        start_listening_text = "RFI Number"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)

    def validate_submittals(self):
        sub_tab_name = "Submittals"
        has_files = True
        start_listening_text = "Sub No"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)


class ValidateJobCostDocs(ValidateESUB):
    tab_name = "Job Cost Docs"

    def __init__(self, project_folder_path) -> None:
        self.project_folder_path = project_folder_path

        self.validate_change_order_requests()
        self.validate_pay_applications()
        self.validate_purchase_orders()
        self.validate_subcontract_change_orders()
        self.validate_subcontracts()

    def validate_change_order_requests(self):
        sub_tab_name = "Change Order Requests"
        has_files = True
        start_listening_text = "Original Contract Amounts"
        skip_text = ["Subtotal", "Grand Total"]
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text, skip_text=skip_text)

    def validate_pay_applications(self):
        sub_tab_name = "Pay Applications"
        has_files = True
        start_listening_text = "Number"
        skip_text = ["Contract Sum to Date"]
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text, skip_text=skip_text)

    def validate_purchase_orders(self):
        sub_tab_name = "Purchase Orders"
        has_files = True
        start_listening_text = "Number"
        skip_text = ["Grand Total"]
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text, skip_text=skip_text)

    def validate_subcontract_change_orders(self):
        sub_tab_name = "Subcontract Change Orders"
        has_files = True
        start_listening_text = "Number"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)

    def validate_subcontracts(self):
        sub_tab_name = "Subcontracts"
        has_files = True
        start_listening_text = "Number"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)


class ValidateProject(ValidateESUB):
    tab_name = "Project"

    def __init__(self, project_folder_path) -> None:
        self.project_folder_path = project_folder_path

        self.validate_emails()
        self.validate_contacts()
        self.validate_issues()

    def validate_emails(self):
        sub_tab_name = "Project Inbox"
        has_files = True
        start_listening_text = "Number"
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text, is_email=True)

    def validate_contacts(self):
        sub_tab_name = "Contacts"
        has_files = True
        start_listening_text = ""
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)

    def validate_issues(self):
        sub_tab_name = "Issues"
        has_files = True
        start_listening_text = ""
        files_folder_path = os.path.join(self.project_folder_path, self.tab_name, sub_tab_name)

        return self._validate(has_files, files_folder_path, start_listening_text)


def validate_all():
    base_path = unp.DOWNLOAD_BASE_FOLDER

    for project_folder_path in list(pathlib.Path(base_path).glob("*")):
        ValidateConstructionDocs(str(project_folder_path))
        ValidateJobCostDocs(str(project_folder_path))
        ValidateProject(str(project_folder_path))


if __name__ == "__main__":
    validate_all()
