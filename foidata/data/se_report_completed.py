from datetime import date, datetime, time, timedelta

from .data import FOIData
from ..service.constants import WEEK_COUNT

class SelfExaminationReport:

    def __init__(self):
        self.data = FOIData()
        self.ser = self.data.self_examination

    '''
        possibly rename this file to se_report.
        create files and subclasses that inherit from SelfExaminationReport
    '''

    @property
    def latest_sunday(self):
        today = date.today()
        offset = (today.weekday() + 1)
        return today - timedelta(days = offset)

    @property
    def past_deadline(self):
        sunday = self.latest_sunday
        time_obj = time(16)
        return datetime.combine(sunday, time_obj)

    def foi_not_completed(self):
        entries_this_week = 'filter self.ser for timestamp >= self.latest_sunday'
        # get list of nation ids from df 
        # filter profile models where profile.nation_id not in list of nation ids that have completed report
