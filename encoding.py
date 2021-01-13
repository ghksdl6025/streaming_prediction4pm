'''
Define class prefix bin to manage subperiod of case by prefix length
'''
import datetime

class prefix_bin:
    def __init__(self):
        self.prefix_length =0
        self.caseid = ''
        self.attrs = {}
        self.enctype = 'Aggregation'
        self.start_ts = ''

    def _update_enctype(self,enctype):
        self.enctype = enctype

    def set_caseid(self, caseid):
        self.caseid = caseid
    
    def set_start_ts(self, start_ts, format=None):
        if isinstance(start_ts, datetime.datetime):
            self.start_ts = start_ts
        else:
            self.start_ts = datetime.datetime.strptime(start_ts, '%Y-%m-%d %H:%M:%S')
    
    def update_attrs(self, event):
        '''
        Assign encoded case and event information to attrs property

        Parameters
        ----------
        event: Dictionary data type
            New event stream 
        '''
        

