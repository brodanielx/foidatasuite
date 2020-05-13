from collections import deque
from datetime import date, datetime, time, timedelta

import pandas as pd

from .data import FOIData
from ..service.constants import WEEK_COUNT
from users.models import Profile

class SelfExaminationReport:

    def __init__(self):
        self.data = FOIData()
        self.ser = self.data.self_examination
        self.latest_sunday = self.get_latest_sunday()
        self.latest_sunday_datetime = datetime.combine(self.latest_sunday, time.min)
        self.weeks_df = self.get_weeks()

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



    def report_completed_by_week(self, week, timestamps):
        start = week
        end = start + timedelta(weeks=1)
        entries = timestamps[(timestamps >= start) & (timestamps < end)]
        print(entries)
        # get latest entry from entries, return 0, 1, or 2
        return 0

    # create class SEReportCompleted(SelfExaminationReport) in new file 