
import pcaspy


class PCASDriver(pcaspy.Driver):

    def __init__(self):
        super().__init__()

    def read(self, reason):
        return super().read(reason)

    def write(self, reason, value):
        if "OutputCurrent" in reason or "CommandMode" in reason or "OnOff" in reason or "HardInterlocks" in reason:
            print(reason + " - Read only PV!")
            return False
        elif "Command" in reason:
            ps = reason.split(":")[0]
            if value == 0:
                pv = ps + ":OnOff"
                self.setParam(pv, 1)
            elif value == 1:
                pv = ps + ":OnOff"
                self.setParam(pv, 0)
            self.updatePVs()
            return super().write(reason, value)
        elif "SlowReferenceCurrent" in reason:
            ps = reason.split(":")[0]
            pv = ps + ":OutputCurrent"
            state = self.getParam(ps+":OnOff")
            if state == 1:
                self.setParam(pv, value)
            self.updatePVs()
            return super().write(reason, value)
