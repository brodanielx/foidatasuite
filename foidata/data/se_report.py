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

        self.data_columns = [
            self.fajr_column,
            self.study_column,
            self.lf_call_column,
            self.exercise_column
        ]

        self.column_abbrvs = {
            self.name_column : 'Name',
            self.nation_id_column : 'NationId',
            self.fajr_column : 'Fajr',
            self.study_column : 'StudyHours',
            self.lf_call_column : 'Calls',
            self.exercise_column : 'ExerciseDays'
        }

    @property
    def past_deadline(self):
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

        column_abbrv = self.column_abbrvs.get(column_name)

        se_df = self.data.se_by_nation_id(nation_id)
        category_df = se_df[['Timestamp', column_name]]
        historical_df = self.weeks_df.copy()

        historical_df[column_abbrv] = historical_df.apply(lambda row: self.individual_by_week_check(row['Week'], category_df, column_name), axis=1)

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
        column_abbrv = self.column_abbrvs.get(column_name)

        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        end_range = ending_sunday + timedelta(days=7)

        se_df = self.ser
        se_df = se_df[(se_df['Timestamp'] >= ending_sunday) & (se_df['Timestamp'] < end_range)]
        category_df = se_df[['Timestamp', self.nation_id_column, column_name]]

        profiles_df = self.userutils.get_profiles_df()
        
        profiles_df[column_abbrv] = profiles_df.apply(lambda row: self.group_single_week_check(row['nation_id'], category_df, column_name), axis=1)

        return profiles_df


    def group_single_week_check(self, nation_id, category_df, column_name):
        entries = category_df[category_df[self.nation_id_column] == nation_id]
        
        if entries.empty:
            return 0
        else:
            return entries[column_name].iloc[-1]


    def individual_single_week_by_category(self, nation_id, column_name, ending_sunday=None):
        column_abbrv = self.column_abbrvs.get(column_name)
        group_df = self.group_single_week(column_name, ending_sunday)
        
        individual_df = group_df[group_df['nation_id'] == nation_id]

        return individual_df[column_abbrv].iloc[0]


    def individual_single_week(self, nation_id, ending_sunday=None):
        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        end_range = ending_sunday + timedelta(days=7)

        se_df = self.ser
        se_df = se_df[(se_df['Timestamp'] >= ending_sunday) & (se_df['Timestamp'] < end_range)]
        se_df = se_df[se_df[self.nation_id_column] == nation_id]

        if not se_df.empty:
            return se_df.tail(1)

        return se_df


    def individual_last_two_weeks(self, nation_id, ending_sunday=None):
        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        previous_ending_sunday = ending_sunday - timedelta(weeks=1)

        current_week_df = self.individual_single_week(nation_id, ending_sunday)
        previous_week_df = self.individual_single_week(nation_id, previous_ending_sunday)

        current_week_records = current_week_df.to_dict('records')
        previous_week_records = previous_week_df.to_dict('records')

        current_week_dict = current_week_records[0] if len(current_week_records) else {}
        previous_week_dict = previous_week_df.to_dict('records')[0]
        current_week_dict = self.abbreviate_keys(current_week_dict)
        previous_week_dict = self.abbreviate_keys(previous_week_dict)

        print(nation_id)
        print(current_week_dict)
        print(previous_week_dict)
        print('\n')

        return 0

    
    def abbreviate_keys(self, dict_obj):

        if not dict_obj:
            return dict_obj

        abbrv_dict = {}

        for k, v in dict_obj:
            abbrv = self.column_abbrvs.get(k)
            
            if abbrv:
                abbrv_dict[abbrv] = v
            else:
                abbrv_dict[k] = v 
        
        return abbrv_dict