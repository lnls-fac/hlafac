
from utils import log
import threading
import api_pv as _api_pv
import api_correction as _api_correction
from time import sleep
from collections import deque
from numpy import array, mean, sqrt, square
from pcaspy import Driver
from epics import caput


class CODCorrectionThread(threading.Thread):

    def __init__(self, name, stop_event, interval):
        """Orbit Correction Thread Object

        Keyword arguments:
        name -- threading object's name
        interval -- processing interval [s]
        stop_event -- event to stop processing

        Class main attribute: mode
        Defines what type of correction should be done.
        0-Off, 1-H, 2-V, 3-H_V, 4-HV, 5-H_F, 6-V_F, 7-H_V_F, 8-HV_F
        """

        self._name = name
        super().__init__(name=self._name, target=self._main, daemon=True)
        self._interval = interval
        self._stop_event = stop_event
        self._mode = 0

    def cod_correction(self, ctype = ''):
        if ctype.lower() == 'h' or ctype.lower() == 'h_f':
            orbit = self._driver.getParam('SICO-SOFB-AVGORBIT-X')
        elif ctype.lower() == 'v' or ctype.lower() == 'v_f':
            orbit = self._driver.getParam('SICO-SOFB-AVGORBIT-Y')
        elif ctype.lower() == 'hv' or ctype.lower() == 'hv_f' or ctype.lower() == 'h_v' or ctype.lower() == 'h_v_f':
            orbit = []
            orbit.extend(self._driver.getParam('SICO-SOFB-AVGORBIT-X'))
            orbit.extend(self._driver.getParam('SICO-SOFB-AVGORBIT-Y'))
        delta_kick = _api_correction.calc_kick(orbit, ctype)
        _api_pv.add_kick(delta_kick, ctype)

    def _main(self):
        _api_correction.initialize_slot(var_type = 'all')
        _api_correction.set_reforbit('x')
        self._driver.setParam('SICO-SOFB-REFORBIT-X', _api_correction.get_reforbit('x'))
        _api_correction.set_reforbit('y')
        self._driver.setParam('SICO-SOFB-REFORBIT-Y', _api_correction.get_reforbit('y'))
        _api_correction.set_respm()
        self._driver.setParam('SICO-SOFB-RESPM', _api_correction.get_respm())
        _api_correction.set_inv_respm()
        while not self._stop_event.is_set():
            if self._mode == 1:
                self.cod_correction('h')
            elif self._mode == 2:
                self.cod_correction('v')
            elif self._mode == 3:
                self.cod_correction('h_v')
            elif self._mode == 4:
                self.cod_correction('hv')
            elif self._mode == 5:
                self.cod_correction('h_f')
            elif self._mode == 6:
                self.cod_correction('v_f')
            elif self._mode == 7:
                self.cod_correction('h_v_f')
            elif self._mode == 8:
                self.cod_correction('hv_f')
            else:
                sleep(self._interval)
        else:
            log('exit', 'orbit correction thread')


class MEASOrbitThread(threading.Thread):

    def __init__(self, name, stop_event, interval, n_samples):
        """Orbit Measurement Thread Object

        Keyword arguments:
        name -- threading object's name
        interval -- processing interval [s]
        stop_event -- event to stop processing
        n_samples -- number of measurements to compute orbit average
        """

        self._name = name
        super().__init__(name=self._name, target=self._main, daemon=True)
        self._interval = interval
        self._stop_event = stop_event
        self._n_samples = n_samples
        self._max_length = 100
        self._orbit_buffer = deque(maxlen = self._max_length)

    def average_orbit(self):
        orbit = array(self._orbit_buffer)[-self._n_samples:]
        avg_orbit = mean(orbit, axis=0)
        return avg_orbit

    def _main(self):
        while not self._stop_event.is_set():
            try:
                orbit = _api_pv.get_orbit('xy')
                self._orbit_buffer.append(orbit)
                avg_orbit = self.average_orbit()
                orbit_x = avg_orbit[:len(_api_pv._pvnames_bpm_x)]
                orbit_y = avg_orbit[len(_api_pv._pvnames_bpm_x):]
                self._driver.setParam('SICO-SOFB-AVGORBIT-X', orbit_x)
                self._driver.setParam('SICO-SOFB-AVGORBIT-Y', orbit_y)
                try:
                    delta_x = abs(orbit_x-_api_correction._reforbit_x)
                    delta_y = abs(orbit_y-_api_correction._reforbit_y)
                    self._driver.setParam('SICO-SOFB-ORBIT-X-MEAN', mean(delta_x))
                    self._driver.setParam('SICO-SOFB-ORBIT-Y-MEAN', mean(delta_y))
                    self._driver.setParam('SICO-SOFB-ORBIT-X-MAX', max(delta_x))
                    self._driver.setParam('SICO-SOFB-ORBIT-Y-MAX', max(delta_y))
                    self._driver.setParam('SICO-SOFB-ORBIT-X-MIN', min(delta_x))
                    self._driver.setParam('SICO-SOFB-ORBIT-Y-MIN', min(delta_y))
                    self._driver.setParam('SICO-SOFB-ORBIT-X-RMS', sqrt(mean(square(delta_x))))
                    self._driver.setParam('SICO-SOFB-ORBIT-Y-RMS', sqrt(mean(square(delta_y))))
                except:
                    self._driver.setParam('SICO-SOFB-ERROR', 6)
            except:
                self._driver.setParam('SICO-SOFB-ERROR', 3)
        else:
            log('exit', 'orbit measurement thread')


class MEASRespmThread(threading.Thread):

    def __init__(self, name, stop_event, interval):
        """Orbit Measurement Thread Object

        Keyword arguments:
        name -- threading object's name
        interval -- processing interval [s]
        stop_event -- event to stop processing

        Class main attribute: mode
        Defines what type of respm should be measured.
        0-Off, 1-H, 2-V, 3-HV, 4-H_F, 5-V_F, 6-HV_F
        """

        self._name = name
        super().__init__(name=self._name, target=self._main, daemon = True)
        self._interval = interval
        self._stop_event = stop_event
        self._mode = 0

    def _finalise_meas_respm(self, respm):
        _api_correction.update_respm_slot(respm, reshape = False)
        self._mode = 'Off'
        self._driver.setParam('SICO-SOFB-MEASRESPM', 0)
        print('Response matrix measurement OK.')

    def _main(self):
        while not self._stop_event.is_set():
            if self._mode == 1:
                respm = _api_pv.meas_respm('h')
                self._finalise_meas_respm(respm)
            elif self._mode == 2:
                respm = _api_pv.meas_respm('v')
                self._finalise_meas_respm(respm)
            elif self._mode == 3:
                respm = _api_pv.meas_respm('hv')
                self._finalise_meas_respm(respm)
            elif self._mode == 4:
                respm = _api_pv.meas_respm('h_f')
                self._finalise_meas_respm(respm)
            elif self._mode == 5:
                respm = _api_pv.meas_respm('v_f')
                self._finalise_meas_respm(respm)
            elif self._mode == 6:
                respm = _api_pv.meas_respm('hv_f')
                self._finalise_meas_respm(respm)
            else:
                sleep(self._interval)
        else:
            log('exit', 'response matrix measurement thread')


class UPDATEVariablesThread(threading.Thread):

    def __init__(self, name, stop_event, interval):
        """Variable Update Thread Object

        Keyword arguments:
        name -- threading object's name
        interval -- processing interval [s]
        stop_event -- event to stop processing

        Class main attribute: mode
        Defines what variable should be updated.
        0-Off, 1-respm, 2-reforbit_x, 3-reforbit_y, 4-respm_sel, 5-reforbit_x_sel, 6-reforbit_y_sel
        """

        self._name = name
        super().__init__(name=self._name, target=self._main, daemon = True)
        self._interval = interval
        self._stop_event = stop_event
        self._mode = 0

    def _main(self):
        while not self._stop_event.is_set():
            if self._mode == 1:
                try:
                    _api_correction.update_respm_slot(self._driver.getParam('SICO-SOFB-RESPM'), reshape = True)
                    _api_correction.set_respm()
                    _api_correction.set_inv_respm()
                except:
                    self._driver.setParam('SICO-SOFB-ERROR', 10)
                self._mode = 0
            elif self._mode == 2:
                try:
                    _api_correction.update_reforbit_slot(self._driver.getParam('SICO-SOFB-REFORBIT-X'), 'x')
                    _api_correction.set_reforbit('x')
                except:
                    self._driver.setParam('SICO-SOFB-ERROR', 11)
                self._mode = 0
            elif self._mode == 3:
                try:
                    _api_correction.update_reforbit_slot(self._driver.getParam('SICO-SOFB-REFORBIT-Y'), 'y')
                    _api_correction.set_reforbit('y')
                except:
                    self._driver.setParam('SICO-SOFB-ERROR', 11)
                self._mode = 0
            elif self._mode == 4:
                try:
                    _api_correction.set_respm_slot(self._driver.getParam('SICO-SOFB-RESPM-SEL'))
                    _api_correction.set_respm()
                    self._driver.setParam('SICO-SOFB-RESPM', _api_correction.get_respm())
                    _api_correction.set_inv_respm()
                except:
                    self._driver.setParam('SICO-SOFB-ERROR', 10)
                self._mode = 0
            elif self._mode == 5:
                try:
                    _api_correction.set_reforbit_slot(self._driver.getParam('SICO-SOFB-REFORBIT-X-SEL'), 'x')
                    _api_correction.set_reforbit('x')
                    self.setParam('SICO-SOFB-REFORBIT-X', _api_correction.get_reforbit('x'))
                except:
                    self._driver.setParam('SICO-SOFB-ERROR', 11)
                self._mode = 0
            elif self._mode == 6:
                try:
                    _api_correction.set_reforbit_slot(self._driver.getParam('SICO-SOFB-REFORBIT-Y-SEL'), 'y')
                    _api_correction.set_reforbit('y')
                    self.setParam('SICO-SOFB-REFORBIT-Y', _api_correction.get_reforbit('y'))
                except:
                    self._driver.setParam('SICO-SOFB-ERROR', 11)
                self._mode = 0
            else:
                sleep(self._interval)
        else:
            log('exit', 'update variables thread')
