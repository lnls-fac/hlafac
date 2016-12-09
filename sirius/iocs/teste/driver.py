
import pcaspy
import numpy

class PCASDriver(pcaspy.Driver):

    def __init__(self):
        super().__init__()

    def read(self, reason):
        return super().read(reason)

    def write(self, reason, value):
        if reason == 'EXAMPLEPV1':
            m1 = numpy.ones((1,3))
            m2 = numpy.ones((1,3))*2
            m3 = numpy.ones((1,3))*3
            m = numpy.array((m1,m2,m3))
            self.setParam('EXAMPLEPV3', numpy.transpose(m))
        return super().write(reason, value)
