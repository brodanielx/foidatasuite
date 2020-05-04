
from .data import FOIData
from ..service.constants import WEEK_COUNT

class SelfExaminationReport:

    def __init__(self):
        self.data = FOIData()
        self.ser = self.data.self_examination
        self.deadline = self.get_deadline()

    def get_deadline(self):
        '''Get report deadline for current week.'''
        # use date.isocalendar to determine current week

        pass