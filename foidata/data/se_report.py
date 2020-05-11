from collections import deque
from datetime import date, datetime, time, timedelta

from .data import FOIData
from ..service.constants import WEEK_COUNT
from users.models import Profile

class SelfExaminationReport:

    def __init__(self):
        self.data = FOIData()
        self.ser = self.data.self_examination
        self.latest_sunday = self.get_latest_sunday()
        self.latest_sunday_datetime = datetime.combine(self.latest_sunday, time.min)

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

        return sundays 


    def foi_not_completed(self):
        df = self.ser

        after_latest_sunday = df['Timestamp'] >= self.latest_sunday_datetime

        entries_this_week = df[after_latest_sunday]
        
        nation_id_col = 'Please enter your Nation ID number:'
        nation_ids = entries_this_week[nation_id_col].tolist()
    
        profiles = Profile.objects.filter(receive_emails=True).exclude(nation_id__in=nation_ids)

        return profiles