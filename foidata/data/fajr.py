from datetime import timedelta

import pandas as pd

from .se_report import SelfExaminationReport
from users.models import Profile


class Fajr(SelfExaminationReport):

    def __init__(self):
        super().__init__()
        self.fajr_column = 'How many days did you make Fajr Prayer this week?'

    def individual(self, nation_id):
        se_df = self.data.se_by_nation_id(nation_id)
        fajr_df = se_df[['Timestamp', self.fajr_column]]
        df = self.weeks_df.copy()

        df['Fajr'] = df.apply(lambda row: self.individual_by_week(row['Week'], fajr_df), axis=1)

        x = list(df['Week'])
        y = list(df['Fajr'])

        return x, y

        
    def individual_by_week(self, week, fajr_df):
        start = week
        end = start + timedelta(weeks=1)
        entries = fajr_df[(fajr_df['Timestamp'] >= start) & (fajr_df['Timestamp'] < end)]

        if entries.empty:
            return 0
        else:
            return entries[self.fajr_column].iloc[-1]



    def by_week(self, ending_sunday=None):
        if not ending_sunday:
            ending_sunday = self.latest_sunday_datetime

        end_range = ending_sunday + timedelta(days=7)

        se_df = self.ser
        se_df = se_df[(se_df['Timestamp'] >= ending_sunday) & (se_df['Timestamp'] < end_range)]
        print(se_df)