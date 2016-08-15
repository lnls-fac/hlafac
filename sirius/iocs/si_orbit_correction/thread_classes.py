
from utils import log
import threading
import api_pv as _api_pv
import api_correction as _api_correction
from time import sleep
from collections import deque
import numpy as _np
from pcaspy import Driver
from epics import caput
from re import findall


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
            idx_c = [_api_correction.get_device_idx('ch')]
        elif ctype.lower() == 'v' or ctype.lower() == 'v_f':
            orbit = self._driver.getParam('SICO-SOFB-AVGORBIT-Y')
            idx_c = [_api_correction.get_device_idx('cv')]
        elif ctype.lower() == 'hv' or ctype.lower() == 'hv_f' or ctype.lower() == 'h_v' or ctype.lower() == 'h_v_f':
            orbit = []
            orbit.extend(self._driver.getParam('SICO-SOFB-AVGORBIT-X'))
            orbit.extend(self._driver.getParam('SICO-SOFB-AVGORBIT-Y'))
            idx_c = [_api_correction.get_device_idx('ch'), _api_correction.get_device_idx('cv')]
        delta_kick = _api_correction.calc_kick(_np.array(orbit), ctype)
        _api_pv.add_kick(delta_kick, ctype, idx_c)


    def _main(self):
        _api_correction.initialize_device_sel()
        _api_correction.set_device_sel('all')
        self._driver.setParam('SICO-SOFB-BPM-SEL', _api_correction.get_device_sel('bpm'))
        self._driver.setParam('SICO-SOFB-CH-SEL', _api_correction.get_device_sel('ch'))
        self._driver.setParam('SICO-SOFB-CV-SEL', _api_correction.get_device_sel('cv'))
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
        orbit = _np.array(self._orbit_buffer)[-self._n_samples:]
        avg_orbit = _np.mean(orbit, axis=0)
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
                    delta_x = abs(orbit_x-_api_correction.get_reforbit('x'))
                    delta_y = abs(orbit_y-_api_correction.get_reforbit('y'))
                    self._driver.setParam('SICO-SOFB-ORBIT-X-MEAN', _np.mean(delta_x))
                    self._driver.setParam('SICO-SOFB-ORBIT-Y-MEAN', _np.mean(delta_y))
                    self._driver.setParam('SICO-SOFB-ORBIT-X-MAX', max(delta_x))
                    self._driver.setParam('SICO-SOFB-ORBIT-Y-MAX', max(delta_y))
                    self._driver.setParam('SICO-SOFB-ORBIT-X-MIN', min(delta_x))
                    self._driver.setParam('SICO-SOFB-ORBIT-Y-MIN', min(delta_y))
                    self._driver.setParam('SICO-SOFB-ORBIT-X-RMS', _np.sqrt(_np.mean(_np.square(delta_x))))
                    self._driver.setParam('SICO-SOFB-ORBIT-Y-RMS', _np.sqrt(_np.mean(_np.square(delta_y))))
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
        0-Off, 9-H, 10-V, 11-HV, 12-H_F, 13-V_F, 14-HV_F
        """

        self._name = name
        super().__init__(name=self._name, target=self._main, daemon = True)
        self._interval = interval
        self._stop_event = stop_event
        self._mode = 0
        self._interrupt_measrespm_event = threading.Event()

    def _finalise_meas_respm(self, respm):
        if respm.shape != (0,):
            _respm = _np.zeros((len(_api_pv._pvnames_bpm_x)+len(_api_pv._pvnames_bpm_y), len(_api_pv._pvnames_ch)+len(_api_pv._pvnames_cv)+1))
            if self._mode == 9:
                _respm[:len(_api_pv._pvnames_bpm_x),:len(_api_pv._pvnames_ch)] = respm
            elif self._mode == 10:
                _respm[len(_api_pv._pvnames_bpm_x):,len(_api_pv._pvnames_ch):-1] = respm
            elif self._mode == 11:
                _respm[:,:-1] = respm
            elif self._mode == 12:
                _respm[:len(_api_pv._pvnames_bpm_x),:len(_api_pv._pvnames_ch)] = respm[:,:-1]
                _respm[:len(_api_pv._pvnames_bpm_x),-1] = respm[:,-1]
            elif self._mode == 13:
                _respm[len(_api_pv._pvnames_bpm_x):,len(_api_pv._pvnames_ch):-1] = respm[:,:-1]
                _respm[len(_api_pv._pvnames_bpm_x):,-1] = respm[:,-1]
            elif self._mode == 14:
                _respm = respm
            self._driver.write('SICO-SOFB-RESPM', _respm)
        self._interrupt_measrespm_event.clear()
        self._mode = 0
        self._driver.setParam('SICO-SOFB-MODE', 0)

    def _main(self):
        while not self._stop_event.is_set():
            if self._mode == 9:
                respm = _api_pv.meas_respm('h', self._interrupt_measrespm_event)
                self._finalise_meas_respm(respm)
            elif self._mode == 10:
                respm = _api_pv.meas_respm('v', self._interrupt_measrespm_event)
                self._finalise_meas_respm(respm)
            elif self._mode == 11:
                respm = _api_pv.meas_respm('hv', self._interrupt_measrespm_event)
                self._finalise_meas_respm(respm)
            elif self._mode == 12:
                respm = _api_pv.meas_respm('h_f', self._interrupt_measrespm_event)
                self._finalise_meas_respm(respm)
            elif self._mode == 13:
                respm = _api_pv.meas_respm('v_f', self._interrupt_measrespm_event)
                self._finalise_meas_respm(respm)
            elif self._mode == 14:
                respm = _api_pv.meas_respm('hv_f', self._interrupt_measrespm_event)
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
        0-Off, 1-respm, 2-reforbit_x, 3-reforbit_y, 4-respm_sel, 5-reforbit_x_sel, 6-reforbit_y_sel, 7-bpm_sel, 8-ch_sel, 9-cv_sel, 10-add_bpm, 11-add_ch, 12-add_cv, 13-rmv_bpm, 14-rmv_ch 15-rmv_cv
        """

        self._name = name
        super().__init__(name=self._name, target=self._main, daemon = True)
        self._interval = interval
        self._stop_event = stop_event
        self._mode = 0

    def _main(self):
        while not self._stop_event.is_set():
            if self._mode != 0:
                if self._mode == 1:
                    try:
                        _api_correction.update_respm_slot(self._driver.getParam('SICO-SOFB-RESPM'), reshape = True)
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 10)
                elif self._mode == 2:
                    try:
                        _api_correction.update_reforbit_slot(self._driver.getParam('SICO-SOFB-REFORBIT-X'), 'x')
                        _api_correction.set_reforbit('x')
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 11)
                elif self._mode == 3:
                    try:
                        _api_correction.update_reforbit_slot(self._driver.getParam('SICO-SOFB-REFORBIT-Y'), 'y')
                        _api_correction.set_reforbit('y')
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 11)
                elif self._mode == 4:
                    try:
                        _api_correction.set_respm_slot(self._driver.getParam('SICO-SOFB-RESPM-SEL'))
                        _api_correction.set_respm()
                        self._driver.setParam('SICO-SOFB-RESPM', _api_correction.get_respm())
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 10)
                elif self._mode == 5:
                    try:
                        _api_correction.set_reforbit_slot(self._driver.getParam('SICO-SOFB-REFORBIT-X-SEL'), 'x')
                        _api_correction.set_reforbit('x')
                        self.setParam('SICO-SOFB-REFORBIT-X', _api_correction.get_reforbit('x'))
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 11)
                elif self._mode == 6:
                    try:
                        _api_correction.set_reforbit_slot(self._driver.getParam('SICO-SOFB-REFORBIT-Y-SEL'), 'y')
                        _api_correction.set_reforbit('y')
                        self.setParam('SICO-SOFB-REFORBIT-Y', _api_correction.get_reforbit('y'))
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 11)
                elif self._mode == 7:
                    try:
                        _api_correction.update_device_sel('bpm', self._driver.getParam('SICO-SOFB-BPM-SEL'))
                        _api_correction.set_device_sel('bpm')
                        _api_correction.set_reforbit('xy')
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                elif self._mode == 8:
                    try:
                        _api_correction.update_device_sel('ch', self._driver.getParam('SICO-SOFB-CH-SEL'))
                        _api_correction.set_device_sel('ch')
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                elif self._mode == 9:
                    try:
                        _api_correction.update_device_sel('cv', self._driver.getParam('SICO-SOFB-CV-SEL'))
                        _api_correction.set_device_sel('cv')
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                elif self._mode == 10:
                    try:
                        _api_correction.change_device_status('bpm', self._driver.getParam('SICO-SOFB-BPM-ADD'), 1)
                        _api_correction.set_device_sel('bpm')
                        self._driver.setParam('SICO-SOFB-BPM-SEL', _api_correction.get_device_sel('bpm'))
                        _api_correction.set_reforbit('xy')
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                elif self._mode == 11:
                    try:
                        _api_correction.change_device_status('ch', self._driver.getParam('SICO-SOFB-CH-ADD'), 1)
                        _api_correction.set_device_sel('ch')
                        self._driver.setParam('SICO-SOFB-CH-SEL', _api_correction.get_device_sel('ch'))
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                elif self._mode == 12:
                    try:
                        _api_correction.change_device_status('cv', self._driver.getParam('SICO-SOFB-CV-ADD'), 1)
                        _api_correction.set_device_sel('cv')
                        self._driver.setParam('SICO-SOFB-CV-SEL', _api_correction.get_device_sel('cv'))
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                elif self._mode == 13:
                    try:
                        _api_correction.change_device_status('bpm', self._driver.getParam('SICO-SOFB-BPM-RMV'), 0)
                        _api_correction.set_device_sel('bpm')
                        self._driver.setParam('SICO-SOFB-BPM-SEL', _api_correction.get_device_sel('bpm'))
                        _api_correction.set_reforbit('xy')
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                elif self._mode == 14:
                    try:
                        _api_correction.change_device_status('ch', self._driver.getParam('SICO-SOFB-CH-RMV'), 0)
                        _api_correction.set_device_sel('ch')
                        self._driver.setParam('SICO-SOFB-CH-SEL', _api_correction.get_device_sel('ch'))
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                elif self._mode == 15:
                    try:
                        _api_correction.change_device_status('cv', self._driver.getParam('SICO-SOFB-CV-RMV'), 0)
                        _api_correction.set_device_sel('cv')
                        self._driver.setParam('SICO-SOFB-CV-SEL', _api_correction.get_device_sel('cv'))
                        _api_correction.set_respm()
                        _api_correction.set_inv_respm()
                    except:
                        self._driver.setParam('SICO-SOFB-ERROR', 12)
                self._mode = 0
                corr_onhold = str(self._driver._threads_dic['orbit_correction']._mode).split('_')
                meas_onhold = str(self._driver._threads_dic['respm_measurement']._mode).split('_')
                if corr_onhold[0] == 'W':
                    self._driver.write('SICO-SOFB-MODE', int(corr_onhold[1]))
                elif meas_onhold[0] == 'W':
                    self._driver.write('SICO-SOFB-MODE', int(meas_onhold[1]))
            else:
                sleep(self._interval)
        else:
            log('exit', 'update variables thread')
