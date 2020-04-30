import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from .constants import (
    CLIENT_SECRET_FILENAME,
    SCOPE,

    CSV_DIRECTORY,
    DUES_CSV_PATH,
    FCN_CSV_PATH,
    FOI_CLASS_ATTENDANCE_CSV_PATH,
    ROSTER_CSV_PATH,
    SELF_EXAMINATION_CSV_PATH,

    DUES_SHEET_TITLE,
    FCN_SHEET_TITLE,
    FOI_CLASS_ATTENDANCE_SHEET_TITLE,
    ROSTER_SHEET_TITLE,
    ROSTER_WORKSHEET_TITLE,
    SELF_EXAMINATION_SHEET_TITLE,

    WORKSHEETS_TO_EXCLUDE,
    WEEK_COUNT
)


class GoogleSheetsToCSVService:

    def __init__(self):
        self.client = self.get_client()

        if not os.path.exists(CSV_DIRECTORY):
            os.mkdir(CSV_DIRECTORY)


    def get_client(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CLIENT_SECRET_FILENAME, SCOPE
        )
        return gspread.authorize(credentials)

    def dues(self):
        sheet = self.client.open(DUES_SHEET_TITLE)
        df = self.sheet_to_df(sheet, WORKSHEETS_TO_EXCLUDE)
        df.to_csv(DUES_CSV_PATH, index=False)

    def fcn(self):
        sheet = self.client.open(FCN_SHEET_TITLE)
        df = self.sheet_to_df(sheet, WORKSHEETS_TO_EXCLUDE)
        df.to_csv(FCN_CSV_PATH, index=False)

    def foi_class_attendance(self):
        sheet = self.client.open(FOI_CLASS_ATTENDANCE_SHEET_TITLE)
        df = self.sheet_to_df(sheet, WORKSHEETS_TO_EXCLUDE)
        df.to_csv(FOI_CLASS_ATTENDANCE_CSV_PATH, index=False)

    def roster(self):
        sheet = self.client.open(ROSTER_SHEET_TITLE)
        worksheet = sheet.worksheet(ROSTER_WORKSHEET_TITLE)

        df = self.worksheet_to_df(worksheet)
        df.to_csv(ROSTER_CSV_PATH, index=False)


    def self_examination(self):
        df = self.sheet_by_title(SELF_EXAMINATION_SHEET_TITLE, 500)
        df.to_csv(SELF_EXAMINATION_CSV_PATH, index=False)

    def sheet_by_title(self, sheet_title, week_count=WEEK_COUNT):
        sheet = self.client.open(sheet_title)
        return self.sheet_to_df(sheet, WORKSHEETS_TO_EXCLUDE, week_count)

    def sheet_to_df(self, sheet, worksheets_to_exlucde=None, week_count=WEEK_COUNT):
        worksheet_dfs = []

        if worksheets_to_exlucde:
            worksheets = [ws for ws in sheet.worksheets() if ws.title not in worksheets_to_exlucde]
        else:
            worksheets = sheet.worksheets()

        for worksheet in worksheets:
            worksheet_df = self.worksheet_to_df(worksheet)
            worksheet_dfs.append(worksheet_df)

        df = pd.concat(worksheet_dfs, axis=1)
        df = df.loc[:, ~df.columns.duplicated()]

        return df.tail(week_count)

    def worksheet_to_df(self, worksheet):
        data_lists = worksheet.get_all_values()
        column_names = data_lists.pop(0)

        return pd.DataFrame(data_lists, columns=column_names)

