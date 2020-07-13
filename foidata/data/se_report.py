from collections import deque
from datetime import date, datetime, time, timedelta

import pandas as pd

from .data import FOIData
from ..service.constants import WEEK_COUNT
from users.models import Profile
from users.utils import UserUtils

class SelfExaminationReport:

    def __init__(self):
        self.data = FOIData()
        self.ser = self.data.self_examination
        self.latest_sunday = self.data.get_latest_sunday()
        self.latest_sunday_datetime = datetime.combine(self.latest_sunday, time.min)
        self.weeks_df = self.get_weeks()
        self.userutils = UserUtils()

        self.name_column = 'Please enter your first and last name:'
        self.nation_id_column = 'Please enter your Nation ID number:'
        self.fajr_column = 'How many days did you make Fajr Prayer this week?'
        self.study_column = 'How many hours did you study (read) literature from The Life Giving Teachings of The Most Honorable Elijah Muhammad this week?'
        self.lf_call_column = 'How many Lost Found Brothers did you call and invite to The Teachings this week?'
        self.exercise_column = 'How many days did you exercise this week?'

        fajr_col_abbrv = 'Fajr'
        study_col_abbrv = 'StudyHours'
        lf_call_col_abbrv = 'Calls'
        exercise_col_abbrv = 'ExerciseDays'
        self.report_completed_col = 'ReportCompleted'

        self.column_abbrvs = {
            self.name_column : 'Name',
            self.nation_id_column : 'NationId',
            self.fajr_column : fajr_col_abbrv,
            self.study_column : study_col_abbrv,
            self.lf_call_column : lf_call_col_abbrv,
            self.exercise_column : exercise_col_abbrv
        }

        self.ser = self.ser.rename(columns=self.column_abbrvs)

        self.goals = {
            self.report_completed_col: 2,
            fajr_col_abbrv: 7,
            study_col_abbrv: 5,
            lf_call_col_abbrv: 10,
            exercise_col_abbrv: 7
        }

    @property
    def deadline(self):
        sunday = self.latest_sunday
        time_obj = time(16)
        return datetime.combine(sunday, time_obj)

    def get_weeks(self):
        latest_sunday_dt = self.latest_sunday_datetime
        queue = deque()
        for i in range(WEEK_COUNT + 1):
            sunday = latest_sunday_dt - timedelta(weeks = i)
            queue.appendleft(sunday)

        sundays = list(queue)

        df = pd.DataFrame(sundays, columns=['Week'])

        return df 


    def individual_historical(self, nation_id, column_name):

        se_df = self.data.se_by_nation_id(nation_id)
        se_df = se_df.rename(columns=self.column_abbrvs)

        category_df = se_df[['Timestamp', column_name]]
        historical_df = self.weeks_df.copy()

        historical_df[column_name] = historical_df.apply(lambda row: self.individual_by_week_check(row['Week'], category_df, column_name), axis=1)

        return historical_df


    def individual_by_week_check(self, week, category_df, column_name):
        start = week
        end = start + timedelta(weeks=1)
        entries = category_df[(category_df['Timestamp'] >= start) & (category_df['Timestamp'] < end)]

        if entries.empty:
            return 0
        else:
            return entries[column_name].iloc[-1]


    def group_single_week(self, column_name, ending_sunday=None):

        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        end_range = ending_sunday + timedelta(days=7)

        se_df = self.ser
        se_df = se_df[(se_df['Timestamp'] >= ending_sunday) & (se_df['Timestamp'] < end_range)]
        category_df = se_df[['Timestamp', 'NationId', column_name]]

        profiles_df = self.userutils.get_profiles_df()
        
        profiles_df[column_name] = profiles_df.apply(lambda row: self.group_single_week_check(row['nation_id'], category_df, column_name), axis=1)

        return profiles_df


    def group_single_week_check(self, nation_id, category_df, column_name):
        entries = category_df[category_df['NationId'] == nation_id]
        
        if entries.empty:
            return 0
        else:
            return entries[column_name].iloc[-1]


    def individual_single_week_by_category(self, nation_id, column_name, ending_sunday=None):
        group_df = self.group_single_week(column_name, ending_sunday)
        
        individual_df = group_df[group_df['nation_id'] == nation_id]

        return individual_df[column_name].iloc[0]


    def individual_single_week(self, nation_id, ending_sunday=None):
        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        end_range = ending_sunday + timedelta(days=7)

        se_df = self.ser
        se_df = se_df[(se_df['Timestamp'] >= ending_sunday) & (se_df['Timestamp'] < end_range)]
        se_df = se_df[se_df['NationId'] == nation_id]

        if not se_df.empty:
            se_df = se_df.tail(1)
        else:
            se_df = self.add_zero_row(se_df)

        se_df = self.add_report_completed_cols(se_df, ending_sunday)

        return self.add_grades(se_df)

    
    def add_report_completed_cols(self, df, ending_sunday=None):
        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        deadline = datetime.combine(ending_sunday, time(16))

        df[self.report_completed_col] = df.apply(lambda row: self.report_completed_val(row['Timestamp'], deadline), axis=1)
        df['ReportCompletedStatus'] = df.apply(lambda row: self.report_completed_status(row[self.report_completed_col]), axis=1)
        return df

    def report_completed_val(self, timestamp_val, deadline):
        
        if not timestamp_val:
            return 0
        elif timestamp_val > deadline:
            return 1
        else:
            return 2

    def report_completed_status(self, report_completed_val):
        if report_completed_val == 0:
            return 'Not submitted'
        elif report_completed_val == 1:
            return 'Late'
        elif report_completed_val == 2:
            return 'On time'


    def add_grades(self, df):
        
        for col, goal in self.goals.items():
            grade_col = f'{col}_grade'
            df[grade_col] = df[col] / goal * 100

        return df


    def individual_last_two_weeks(self, nation_id, ending_sunday=None):
        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        previous_ending_sunday = ending_sunday - timedelta(weeks=1)

        current_week_df = self.individual_single_week(nation_id, ending_sunday)
        previous_week_df = self.individual_single_week(nation_id, previous_ending_sunday)

        current_week_dict = current_week_df.to_dict('records')[0]
        previous_week_dict = previous_week_df.to_dict('records')[0]
        differences = self.generate_differences(current_week_dict, previous_week_dict)

        context = {
            'current_week': current_week_dict,
            'previous_week': previous_week_dict,
            'differences': differences
        }

        return context

    
    def generate_differences(self, dict1, dict2):
        differences = {}

        columns = [k for k in self.goals if k != self.report_completed_col]

        for col in columns:
            grade_col = f'{col}_grade'
            differences[col] = dict1[grade_col] - dict2[grade_col]
        
        return differences


    def add_zero_row(self, df):
        dict_obj = {}

        for col in df.columns:
            dict_obj[col] = 0

        return df.append(dict_obj, ignore_index=True)