
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
            if value == 'Off' or value == 0:
                self._threads_dic['orbit_correction']._mode = 'Off'
                print('Orbit correction has stopped.')
            elif value == 'OnH' or value == 1:
                self._threads_dic['orbit_correction']._mode = 'OnH'
                print('Horizontal orbit correction has started.')
            elif value == 'OnV' or value == 2:
                self._threads_dic['orbit_correction']._mode = 'OnV'
                print('Vertical orbit correction has started.')
            elif value == 'OnHOnV' or value == 3:
                self._threads_dic['orbit_correction']._mode = 'OnHOnV'
                print('Horizontal and vertical orbit corrections have started.')
            elif value == 'OnHV' or value == 4:
                self._threads_dic['orbit_correction']._mode = 'OnHV'
                print('Full orbit correction has started.')
            elif value == 'OnH_F' or value == 5:
                self._threads_dic['orbit_correction']._mode = 'OnH_F'
                print('Horizontal orbit correction with RF frequency adjustment has started.')
            elif value == 'OnV_F' or value == 6:
                self._threads_dic['orbit_correction']._mode = 'OnV_F'
                print('Vertical orbit correction with RF frequency adjustment has started.')
            elif value == 'OnHOnV_F' or value == 7:
                self._threads_dic['orbit_correction']._mode = 'OnHOnV_F'
                print('Horizontal and vertical orbit corrections with RF frequency adjustment have started.')
            elif value == 'OnHV_F' or value == 8:
                self._threads_dic['orbit_correction']._mode = 'OnHV_F'
                print('Full orbit correction with RF frequency adjustment has started.')
        elif reason == 'SICO-SOFB-AVGORBIT-NUMSAMPLES':
            if value > self._threads_dic['orbit_measurement']._max_length:
                self.setParam('SICO-SOFB-ERROR', 2)
                return
            else:
                self._threads_dic['orbit_measurement']._n_samples = value
        elif reason == 'SICO-SOFB-MEASRESPM':
            if value == 'Off' or value == 0:
                self._threads_dic['respm_measurement']._mode = 'Off'
            else:
                if self._threads_dic['orbit_correction']._mode != 'Off':
                    self.setParam('SICO-SOFB-ERROR', 1)
                    return
                else:
                    if value == 'OnH' or value == 1:
                        print('Measuring horizontal response matrix...')
                        self._threads_dic['respm_measurement']._mode = 'OnH'
                    elif value == 'OnV' or value == 2:
                        print('Measuring vertical response matrix...')
                        self._threads_dic['respm_measurement']._mode = 'OnV'
                    elif value == 'OnHV' or value == 3:
                        print('Measuring full response matrix...')
                        self._threads_dic['respm_measurement']._mode = 'OnHV'
                    elif value == 'OnH_F' or value == 4:
                        print('Measuring horizontal response matrix with RF frequency adjustment...')
                        self._threads_dic['respm_measurement']._mode = 'OnH_F'
                    elif value == 'OnV_F' or value == 5:
                        print('Measuring vertical response matrix with RF frequency adjustment...')
                        self._threads_dic['respm_measurement']._mode = 'OnV_F'
                    elif value == 'OnHV_F' or value == 6:
                        print('Measuring full response matrix with RF frequency adjustment...')
                        self._threads_dic['respm_measurement']._mode = 'OnHV_F'
        elif reason == 'SICO-SOFB-RESPM':
            try:
                _api_correction.set_respm(value)
                self._threads_dic['orbit_correction']._respm = value
            except:
                self.setParam('SICO-SOFB-ERROR', 4)
                return
        return super().write(reason, value)
