from datetime import date, datetime, time, timedelta

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
        self.latest_sunday = self.get_latest_sunday()
        self.latest_sunday_datetime = datetime.combine(self.latest_sunday, time.min)

    def get_latest_sunday(self):
        today = date.today()
        offset = (today.weekday() + 1)
        return today - timedelta(days = offset)

    @property
    def roster(self):
        df = pd.read_csv(ROSTER_CSV_PATH)
        df['NationId'] = df.apply(lambda row: self.clean_nation_id(row), axis=1)
        return df

    @property
    def dues(self):
        df = pd.read_csv(DUES_CSV_PATH)
        df = self.clean_df(df)
        df['Week'] = pd.to_datetime(df['Week'])
        df = self.add_total_column(df)
        return df.tail(WEEK_COUNT)

    @property
    def foi_class_attendance(self):
        df = pd.read_csv(FOI_CLASS_ATTENDANCE_CSV_PATH)
        df = self.clean_df(df)
        df['Week'] = pd.to_datetime(df['Week'])
        df = self.add_total_column(df)
        return df.tail(WEEK_COUNT)

    @property
    def fcn(self):
        df = pd.read_csv(FCN_CSV_PATH)
        df = self.clean_df(df)
        df['Week'] = pd.to_datetime(df['Week'])
        df = self.add_total_column(df)
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

    def se_by_nation_id(self, nation_id):
        df = self.self_examination.copy()

        nation_id_col = 'Please enter your Nation ID number:'
        filter_by_nation_id = df[nation_id_col] == nation_id

        return df[filter_by_nation_id] 


    def clean_nation_id(self, row):
        if not row['NationId']:
            first_name_abbr = row['FirstName'][:2].lower()
            last_name_initial = row['LastName'][0].lower()
            return f'{first_name_abbr}{last_name_initial}sp'
        
        return row['NationId']

    def clean_df(self, df):
        df = df.replace(r'', 0)

        return df


    def add_total_column(self, df):
        if 'Total' in df.columns:
            df.drop(columns=['Total'], inplace=True)

        columns = df.columns
        df['Total'] = df.apply(lambda row: self.sum_columns(row, columns), axis=1)

        return df


    def sum_columns(self, row, columns):
        columns = [col for col in columns if col != 'Week']
        total = 0
        for col in columns:
            total += row[col]

        return total

    def get_df_by_category(self, category):
        dfs_by_category = {
            'FOIClassAttendance' : self.foi_class_attendance.copy(),
            'Dues' : self.dues.copy(),
            'FCN' : self.fcn.copy()
        }

        return dfs_by_category[category]

    def group_historical_by_category(self, category):
        df = self.get_df_by_category(category)
        df = df[['Week', 'Total']]
        return df 


    def individual_historical_by_category(self, category, profile_column_header):
        df = self.get_df_by_category(category)
        df = df[['Week', profile_column_header]]
        return df


    def group_single_week_by_category(self, category, ending_sunday=None):
        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        end_range = ending_sunday + timedelta(days=7)

        df = self.get_df_by_category(category)
        df = df[(df['Week'] >= ending_sunday) & (df['Week'] < end_range)]
        
        return df.iloc[0]

    
    def individual_single_week_by_category(self, category, nation_id, ending_sunday=None):
        series = self.group_single_week_by_category(category, ending_sunday)
        s_dict = series.to_dict()
        values = [
            s_dict[k] for k in s_dict 
            if self.is_nation_id_match_str(nation_id, k)
        ]
        return values[0]

    def is_nation_id_match_str(self, nation_id, column):
        # TODO: add nation ids to all spreadsheet columns
        col_nation_id = column.split(' - ')[0]
        try:
            col_nation_id = int(col_nation_id)
            return nation_id == col_nation_id
        except:
            return False


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
    - FCN
        - bar graph - most recent week for all FOI
        - line graph - last n weeks for all FOI total
        - line graph - last n weeks for each FOI individually
'''