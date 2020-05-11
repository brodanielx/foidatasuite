

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
        return df.tail(WEEK_COUNT)

    @property
    def foi_class_attendance(self):
        df = pd.read_csv(FOI_CLASS_ATTENDANCE_CSV_PATH)
        df = self.clean_df(df)
        return df.tail(WEEK_COUNT)

    @property
    def fcn(self):
        df = pd.read_csv(FCN_CSV_PATH)
        df = self.clean_df(df)
        return df.tail(WEEK_COUNT)

    @property
    def self_examination(self):
        df = pd.read_csv(SELF_EXAMINATION_CSV_PATH)
        df = self.clean_df(df)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df 

    def foi_by_nation_id(self, nation_id):
        roster = self.roster
        filter_by_nation_id = roster['NationId'] == nation_id

        try:
            foi = roster[filter_by_nation_id].iloc[0]
            return foi
        except IndexError:
            print(f'Error: There is no FOI with the NationId of {nation_id}')
            return pd.Series([])


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

        return df


'''
Data to collect:
    - Self Examination
        - for all se data
            - create new df for each foi - fill in weeks
                - create new df with 'week' column = se.get_weeks()
                - get data_df for individual foi for specific category (ex: timestamp, fajr, etc)
                - apply lambda funtion to df => check for entry in data_df for each week,
                  update column (ex: report completed, fajr, hours studied, etc) accordingly
        - Report completed / completed on time
            - list of FOI that have not completed report for current week
                - not completed, late, on time
            - line graph 
                - 3 levels on y axis: not submitted 0, late 1, on time 2
                - last n weeks for each FOI individually  
        - Fajr prayer
            - bar graph - most recent week for all FOI
            - histogram - most recent week for all FOI
            - line graph - last n weeks for each FOI individaully
        - Hours studied
            - bar graph - most recent week for all FOI
            - histogram - most recent week for all FOI
            - line graph - last n weeks for each FOI individaully
        - Lost Found Brothers called
            - bar graph - most recent week for all FOI
            - histogram - most recent week for all FOI
            - line graph - last n weeks for each FOI individaully
        - Days exercised
            - bar graph - most recent week for all FOI
            - histogram - most recent week for all FOI
            - line graph - last n weeks for each FOI individaully
        - Hours soldiered (corner)
            - bar graph - most recent week for all FOI
            - line graph - last n weeks for all FOI total
            - line graph - last n weeks for each FOI individually
        - Hours soldiered (door to door)
            - bar graph - most recent week for all FOI
            - line graph - last n weeks for all FOI total
            - line graph - last n weeks for each FOI individually

    - FOI Class Attendance
        - line graph - last n weeks for all FOI total
        - line graph - last n weeks for each FOI individually
    - FOI Dues
        - bar graph - most recent week for all FOI
        - line graph - last n weeks for all FOI total
        - line graph - last n weeks for each FOI individually
'''