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


    

    # create class SEReportCompleted(SelfExaminationReport) in new file 