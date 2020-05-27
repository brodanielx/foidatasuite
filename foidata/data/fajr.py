from datetime import timedelta

import pandas as pd

from .se_report import SelfExaminationReport
from users.models import Profile
from users.utils import UserUtils


class Fajr(SelfExaminationReport):

    def __init__(self):
        super().__init__()
        self.fajr_column = 'How many days did you make Fajr Prayer this week?'
        self.userutils = UserUtils()

    def individual_historical(self, nation_id):
        se_df = self.data.se_by_nation_id(nation_id)
        fajr_df = se_df[['Timestamp', self.fajr_column]]
        df = self.weeks_df.copy()

        df['Fajr'] = df.apply(lambda row: self.individual_by_week_check(row['Week'], fajr_df), axis=1)

        return df

        
    def individual_by_week_check(self, week, fajr_df):
        start = week
        end = start + timedelta(weeks=1)
        entries = fajr_df[(fajr_df['Timestamp'] >= start) & (fajr_df['Timestamp'] < end)]

        if entries.empty:
            return 0
        else:
            return entries[self.fajr_column].iloc[-1]



    def single_week_group(self, ending_sunday=None):
        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        end_range = ending_sunday + timedelta(days=7)

        se_df = self.ser
        se_df = se_df[(se_df['Timestamp'] >= ending_sunday) & (se_df['Timestamp'] < end_range)]
        fajr_df = se_df[['Timestamp', self.nation_id_column, self.fajr_column]]

        profiles_df = self.userutils.get_profiles_df()
        
        profiles_df['Fajr'] = profiles_df.apply(lambda row: self.single_week_group_check(row['nation_id'], fajr_df), axis=1)

        return profiles_df

    
    def single_week_group_check(self, nation_id, fajr_df):
        entries = fajr_df[fajr_df[self.nation_id_column] == nation_id]
        
        if entries.empty:
            return 0
        else:
            return entries[self.fajr_column].iloc[-1]