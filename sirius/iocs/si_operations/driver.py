
import pcaspy
import pvs


class PCASDriver(pcaspy.Driver):
    
    def __init__(self):
        super().__init__()
        self._initialise_pvs()
        
    def read(self, reason):
        return super().read(reason)
         
    def write(self, reason, value):
        return super().write(reason, value)

    def _initialise_pvs(self):
        self.setParam('SHIFT-TYPE', 0)
        self.setParam('MESSAGE', pvs.pvdb['MESSAGE']['value'])
        self.updatePVs()
