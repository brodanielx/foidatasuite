from datetime import timedelta

import pandas as pd

from .se_report import SelfExaminationReport
from users.models import Profile



class SEReportCompleted(SelfExaminationReport):

    def foi_not_completed(self):
        df = self.ser

        after_latest_sunday = df['Timestamp'] >= self.latest_sunday_datetime

        entries_this_week = df[after_latest_sunday]
        
        nation_id_col = 'Please enter your Nation ID number:'
        nation_ids = entries_this_week[nation_id_col].tolist()
    
        profiles = Profile.objects.filter(receive_emails=True).exclude(nation_id__in=nation_ids)

        return profiles


    def report_completed(self, nation_id):
        se_df = self.data.se_by_nation_id(nation_id)
        timestamps = se_df['Timestamp']
        df = self.weeks_df.copy()
        
        df['ReportCompleted'] = df.apply(lambda row: self.report_completed_by_week(row['Week'], timestamps), axis=1)

        return df



    def report_completed_by_week(self, week, timestamps):
        start = week
        end = start + timedelta(weeks=1)
        entries = timestamps[(timestamps >= start) & (timestamps < end)]

        if entries.empty:
            return 0

        entry = entries.iloc[0]
        deadline = start + timedelta(hours=16)
        
        if entry > deadline:
            return 1
        else:
            return 2

