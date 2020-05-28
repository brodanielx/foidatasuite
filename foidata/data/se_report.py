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
        self.latest_sunday = self.get_latest_sunday()
        self.latest_sunday_datetime = datetime.combine(self.latest_sunday, time.min)
        self.weeks_df = self.get_weeks()
        self.profiles = Profile.objects.active()

        self.name_column = 'Please enter your first and last name:'
        self.nation_id_column = 'Please enter your Nation ID number:'
        self.fajr_column = 'How many days did you make Fajr Prayer this week?'
        self.study_column = 'How many hours did you study (read) literature from The Life Giving Teachings of The Most Honorable Elijah Muhammad this week?'
        self.lf_call_column = 'How many Lost Found Brothers did you call and invite to The Teachings this week?'
        self.exercise_column = 'How many days did you exercise this week?'

        self.column_abbrvs = {
            self.name_column : 'Name',
            self.nation_id_column : 'NationId',
            self.fajr_column : 'Fajr',
            self.study_column : 'StudyHours',
            self.lf_call_column : 'Calls',
            self.exercise_column : 'ExerciseDays'
        }

    def get_latest_sunday(self):
        today = date.today()
        offset = (today.weekday() + 1)
        return today - timedelta(days = offset)

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


    # TODO: add remaining Fajr() methods here to have them in one place and not for every category