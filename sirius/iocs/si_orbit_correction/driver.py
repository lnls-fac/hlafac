
import queue
from pcaspy import Driver
import epics
from time import sleep
import api_correction as _api_correction


class PCASDriver(Driver):

    def  __init__(self, threads_dic, start_event, stop_event, interval):
        super().__init__()
        self._threads_dic = threads_dic
        self._interval = interval
        self._start_event = start_event
        self._queue = queue.Queue()
        self._stop_event = stop_event
        for tn in threads_dic:
            self._threads_dic[tn]._driver = self

    def read(self, reason):
        return super().read(reason)

    def write(self, reason, value):
        if reason == 'SICO-SOFB-STATUS':
            if value == 0:
                self._threads_dic['orbit_correction']._mode = value
            else:
                if self._threads_dic['respm_measurement']._mode != 0:
                    self.setParam('SICO-SOFB-ERROR', 7)
                    return
                else:
                    self._threads_dic['orbit_correction']._mode = value
        elif reason == 'SICO-SOFB-AVGORBIT-NUMSAMPLES':
            if value > self._threads_dic['orbit_measurement']._max_length:
                self.setParam('SICO-SOFB-ERROR', 2)
                return
            else:
                self._threads_dic['orbit_measurement']._n_samples = value
        elif reason == 'SICO-SOFB-MEASRESPM':
            if value == 0:
                self._threads_dic['respm_measurement']._mode = value
            else:
                if self._threads_dic['orbit_correction']._mode != 0:
                    self.setParam('SICO-SOFB-ERROR', 1)
                    return
                else:
                    self._threads_dic['respm_measurement']._mode = value
        elif reason == 'SICO-SOFB-RESPM':
            try:
                _api_correction.set_respm(value)
                self._threads_dic['orbit_correction']._respm = value
            except:
                self.setParam('SICO-SOFB-ERROR', 4)
                return
        elif reason == 'SICO-SOFB-REFORBIT-X':
            try:
                _api_correction.set_reference_orbit(value, 'x')
                self._threads_dic['orbit_correction']._reforbitx = value
            except:
                self.setParam('SICO-SOFB-ERROR', 5)
                return
        elif reason == 'SICO-SOFB-REFORBIT-Y':
            try:
                _api_correction.set_reference_orbit(value, 'y')
                self._threads_dic['orbit_correction']._reforbity = value
            except:
                self.setParam('SICO-SOFB-ERROR', 5)
                return
        return super().write(reason, value)
