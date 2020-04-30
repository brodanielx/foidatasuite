

import pandas as pd

from ..service.constants import (
    CSV_DIRECTORY,
    DUES_CSV_PATH,
    FCN_CSV_PATH,
    FOI_CLASS_ATTENDANCE_CSV_PATH,
    ROSTER_CSV_PATH,
    SELF_EXAMINATION_CSV_PATH,
    
    WEEK_COUNT
)


class FOIData:

    def __init__(self):
        pass

    @property
    def roster(self):
        df = pd.read_csv(ROSTER_CSV_PATH)
        df['NationId'] = df.apply(lambda row: self.clean_nation_id(row), axis=1)
        return df

    @property
    def dues(self):
        df = pd.read_csv(DUES_CSV_PATH)
        df = self.clean_df(df)
        return df 

    @property
    def foi_class_attendance(self):
        df = pd.read_csv(FOI_CLASS_ATTENDANCE_CSV_PATH)
        df = self.clean_df(df)
        return df 

    @property
    def fcn(self):
        df = pd.read_csv(FCN_CSV_PATH)
        df = self.clean_df(df)
        return df 

    @property
    def self_examination(self):
        df = pd.read_csv(SELF_EXAMINATION_CSV_PATH)
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