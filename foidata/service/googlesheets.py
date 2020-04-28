import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

from .constants import (
    CLIENT_SECRET_FILENAME,
    SCOPE,

    DUES_SHEET_TITLE,
    FCN_SHEET_TITLE,
    FOI_CLASS_ATTENDANCE_SHEET_TITLE,
    ROSTER_SHEET_TITLE,
    ROSTER_WORKSHEET_TITLE,

    WORKSHEETS_TO_EXCLUDE,
    WEEK_COUNT
)


class GoogleSheetsToCSVService:

    def __init__(self):
        self.client = self.get_client()


    def get_client(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CLIENT_SECRET_FILENAME, SCOPE
        )
        return gspread.authorize(credentials)

    def dues(self):
        sheet = self.client.open(DUES_SHEET_TITLE)
        df = self.sheet_to_df(sheet, WORKSHEETS_TO_EXCLUDE)
        df.to_csv('foidata/csv/dues.csv', index=False)

    def fcn(self):
        sheet = self.client.open(FCN_SHEET_TITLE)
        df = self.sheet_to_df(sheet, WORKSHEETS_TO_EXCLUDE)
        df.to_csv('foidata/csv/fcn.csv', index=False)

    def foi_class_attendance(self):
        sheet = self.client.open(FOI_CLASS_ATTENDANCE_SHEET_TITLE)
        df = self.sheet_to_df(sheet, WORKSHEETS_TO_EXCLUDE)
        df.to_csv('foidata/csv/foiclassattendance.csv', index=False)

    def roster(self):
        sheet = self.client.open(ROSTER_SHEET_TITLE)
        worksheet = sheet.worksheet(ROSTER_WORKSHEET_TITLE)

        df = self.worksheet_to_df(worksheet)
        df.to_csv('foidata/csv/roster.csv', index=False)


    def self_examination(self):
        # get correct google sheet title
        df = self.sheet_by_title('Weekly FOI Report (Responses)')
        df.to_csv('foidata/csv/selfexamination.csv', index=False)

    def sheet_by_title(self, sheet_title):
        sheet = self.client.open(sheet_title)
        return self.sheet_to_df(sheet, WORKSHEETS_TO_EXCLUDE)

    def sheet_to_df(self, sheet, worksheets_to_exlucde=None):
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

        return df.tail(WEEK_COUNT)

    def worksheet_to_df(self, worksheet):
        data_lists = worksheet.get_all_values()
        column_names = data_lists.pop(0)

        return pd.DataFrame(data_lists, columns=column_names)

