#!/usr/bin/env python

'''
TODO: add docs
'''
from fireworks.utilities.fw_serializers import FWSerializable
from fireworks.core.fw_constants import LAUNCH_RANKS
from fireworks.core.fworker import FWorker

__author__ = "Anubhav Jain"
__copyright__ = "Copyright 2013, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Anubhav Jain"
__email__ = "ajain@lbl.gov"
__date__ = "Feb 5, 2013"


class FireWork(FWSerializable):
    
    def __init__(self, fw_spec, fw_id=None, launch_data=None):
        '''
        
        :param fw_spec:
        '''
        self.fw_spec = fw_spec
        self.fw_id = fw_id
        self.launch_data = launch_data if launch_data else []
    
    def to_dict(self):
        return {'fw_spec': self.fw_spec, 'fw_id': self.fw_id, 'launch_data': [l.to_dict() for l in self.launch_data]}
    
    def to_db_dict(self):
        m_dict = self.to_dict()
        m_dict['state'] = self.state
        return m_dict
    
    @classmethod
    def from_dict(self, m_dict):
        
        fw_id = m_dict.get('fw_id', None)
        ld = m_dict.get('launch_data', None)
        if ld:
            ld = [Launch.from_dict(tmp) for tmp in ld]
        return FireWork(m_dict['fw_spec'], fw_id, ld)
    
    @property
    def state(self):
        max_score = 0
        max_state = 'WAITING'
        
        for l in self.launch_data:
            if LAUNCH_RANKS[l.state] > max_score:
                max_score = LAUNCH_RANKS[l.state]
                max_state = l.state 
        
        return max_state
            

#TODO: add date, logs ...
class Launch(FWSerializable):
    
    def __init__(self, fworker, state=None, launch_id=None):
        if state not in LAUNCH_RANKS:
            raise ValueError("Invalid launch state: {}".format(state))
        
        self.fworker = fworker
        self.state = state
        self.launch_id = launch_id
    
    def to_dict(self):
        return {"fworker": self.fworker.to_dict(), "state": self.state, "launch_id": self.launch_id}
    
    @classmethod
    def from_dict(self, m_dict):
        fworker = FWorker.from_dict(m_dict['fworker'])
        return Launch(fworker, m_dict['state'], m_dict['launch_id'])


if __name__ == '__main__':
    fw_spec = {'_script': 'echo "howdy, your job launched successfully!" >> howdy.txt'}
    fw = FireWork(fw_spec)
    fw.to_file("../../fw_tutorial/fw_test.yaml")