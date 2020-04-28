
from .constants import WEEK_COUNT
from ..service.googlesheets import GoogleSheetsService

class FOIData:

    def __init__(self):
        self.svc = GoogleSheetsService()

    @property
    def roster(self):
        df = self.svc.roster()
        df['NationId'] = df.apply(lambda row: self.clean_nation_id(row), axis=1)
        return df

    @property
    def foi_class_attendance(self):
        df = self.svc.foi_class_attendance()
        df = self.clean_df(df)
        return df 

    @property
    def fcn(self):
        df = self.svc.fcn()
        df = self.clean_df(df)
        return df 

    @property
    def self_examination(self):
        df = self.svc.self_examination()
        df = self.clean_df(df)
        return df 


    def fcn_line(self, oi_id=None):
        # x = self.fcn_df['Total]
        # y = self.fcn_df['Week']
        pass 


    def clean_nation_id(self, row):
        if not row['NationId']:
            first_name_abbr = row['FirstName'][:2].lower()
            last_name_initial = row['LastName'][0].lower()
            return f'{first_name_abbr}{last_name_initial}sp'
        
        return row['NationId']

    def clean_df(self, df):
        df = df.replace(r'', 0)
        df = df.tail(WEEK_COUNT)

        return df