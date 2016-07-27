
import os as _os
import lnls as _lnls
import epics as _epics
import numpy as _np
from time import sleep
from datetime import datetime

_PREFIX = 'VA-'
_SUFIX = ''
_SLEEPTIME = 0.1

PV_RF_FREQUENCY = _PREFIX + 'SIRF-FREQUENCY' #virtual accelerator PV
#PV_RF_FREQUENCY = 'DIG-RSSMX100A-0:GENERAL:Freq' #real RF generator PV

_sidi_bpm_devicenames_fname = _os.path.join(_lnls.folder_root,
'siriusdb', 'recordnames_flatlists', 'dname-bpm.txt')
_sips_ch_devicenames_fname  = _os.path.join(_lnls.folder_root,
'siriusdb', 'recordnames_flatlists', 'dname-ch.txt')
_sips_cv_devicenames_fname  = _os.path.join(_lnls.folder_root,
'siriusdb', 'recordnames_flatlists', 'cv.txt')

global _pvs
_pvs = {}


def _read_devicename_file(filename):
    with open(filename, 'r') as fp:
        content = fp.read()
    content = content.splitlines()
    devicenames = []
    for line in content:
        line = line.strip()
        if not line or line[0] == '#': continue
        words = line.split()
        devicenames.append(words[0])
    return devicenames


def _create_pv_names():
    _devicenames_bpm = _read_devicename_file(_sidi_bpm_devicenames_fname)
    _devicenames_ch  = _read_devicename_file(_sips_ch_devicenames_fname)
    _devicenames_cv  = _read_devicename_file(_sips_cv_devicenames_fname)
    pvnames_bpm_x = []
    pvnames_bpm_y = []
    pvnames_ch = []
    pvnames_cv = []
    for i, device in enumerate(_devicenames_bpm):
        pvnames_bpm_x.append(_PREFIX + 'SIDI-' + device + ':MONIT:X')
        pvnames_bpm_y.append(_PREFIX + 'SIDI-' + device + ':MONIT:Y')
        _pvs[pvnames_bpm_x[i]] = _epics.PV(pvnames_bpm_x[i])
        _pvs[pvnames_bpm_y[i]] = _epics.PV(pvnames_bpm_y[i])
    for i, device in enumerate(_devicenames_ch):
        pvnames_ch.append(_PREFIX + 'SIPS-' + device + _SUFIX)
        _pvs[pvnames_ch[i]] = _epics.PV(pvnames_ch[i])
    for i, device in enumerate(_devicenames_cv):
        pvnames_cv.append(_PREFIX + 'SIPS-' + device + _SUFIX)
        _pvs[pvnames_cv[i]] = _epics.PV(pvnames_cv[i])
    _pvs[_PREFIX + 'SIDI-BPM-FAM:MONIT:X'] = _epics.PV(_PREFIX + 'SIDI-BPM-FAM:MONIT:X')
    _pvs[_PREFIX + 'SIDI-BPM-FAM:MONIT:Y'] = _epics.PV(_PREFIX + 'SIDI-BPM-FAM:MONIT:Y')
    _pvs[PV_RF_FREQUENCY] = _epics.PV(PV_RF_FREQUENCY)
    return pvnames_bpm_x, pvnames_bpm_y, pvnames_ch, pvnames_cv


_pvnames_bpm_x, _pvnames_bpm_y, _pvnames_ch, _pvnames_cv = _create_pv_names()


def get_orbit(plane = ''):
    if plane.lower() == 'x':
        orbit = _pvs[_PREFIX + 'SIDI-BPM-FAM:MONIT:X'].value
    elif plane.lower() == 'y':
        orbit = _pvs[_PREFIX + 'SIDI-BPM-FAM:MONIT:Y'].value
    elif plane.lower() == 'xy':
        orbit = []
        orbit.extend(_pvs[_PREFIX + 'SIDI-BPM-FAM:MONIT:X'].value)
        orbit.extend(_pvs[_PREFIX + 'SIDI-BPM-FAM:MONIT:Y'].value)
    return orbit


def get_kick(ctype = ''):
    kick = []
    if ctype.lower() == 'h' or ctype.lower() == 'h_f':
        pvnames_c = _pvnames_ch[:]
        if ctype.lower() == 'h_f':
            pvnames_c.extend([PV_RF_FREQUENCY])
    elif ctype.lower() == 'v' or ctype.lower() == 'v_f':
        pvnames_c = _pvnames_cv[:]
        if ctype.lower() == 'v_f':
            pvnames_c.extend([PV_RF_FREQUENCY])
    elif ctype.lower() == 'hv' or ctype.lower() == 'hv_f' or ctype.lower() == 'h_v' or ctype.lower() == 'h_v_f':
        pvnames_c = []
        pvnames_c.extend(_pvnames_ch)
        pvnames_c.extend(_pvnames_cv)
        if ctype.lower() == 'hv_f' or ctype.lower() == 'h_v_f':
            pvnames_c.extend([PV_RF_FREQUENCY])
    for pvname in pvnames_c:
        kick.append(_pvs[pvname].value)
    return kick


def add_kick(delta_kick = None, ctype = ''):
    if ctype.lower() == 'h' or ctype.lower() == 'h_f':
        pvnames_c = _pvnames_ch[:]
        if ctype.lower() == 'h_f':
            pvnames_c.extend([PV_RF_FREQUENCY])
    elif ctype.lower() == 'v' or ctype.lower() == 'v_f':
        pvnames_c = _pvnames_cv[:]
        if ctype.lower() == 'v_f':
            pvnames_c.extend([PV_RF_FREQUENCY])
    elif ctype.lower() == 'hv' or ctype.lower() == 'hv_f' or ctype.lower() == 'h_v' or ctype.lower() == 'h_v_f':
        pvnames_c = []
        pvnames_c.extend(_pvnames_ch)
        pvnames_c.extend(_pvnames_cv)
        if ctype.lower() == 'hv_f' or ctype.lower() == 'h_v_f':
            pvnames_c.extend([PV_RF_FREQUENCY])
    kick0 = get_kick(ctype)
    for i, pvname in enumerate(pvnames_c):
        kick = kick0[i] + delta_kick[i]
        _pvs[pvname].value = kick
    sleep(5) #delay for update the closed orbit


def _meas_new_orbit(old_orbit, plane):
    while True:
        orbit = _np.array(get_orbit(plane))
        if all(orbit != old_orbit): break
        sleep(_SLEEPTIME)
    return orbit


def meas_respm(ctype = ''):
    sleep(6) #delay for waiting correction finalise
    delta_kick = -0.31833 #hardware units
    #delta_kick = 10e-06 #angle units
    if ctype.lower() == 'h' or ctype.lower() == 'h_f':
        pvnames_bpm = _pvnames_bpm_x[:]
        pvnames_c = _pvnames_ch[:]
        plane = 'x'
    elif ctype.lower() == 'v' or ctype.lower() == 'v_f':
        pvnames_bpm = _pvnames_bpm_y[:]
        pvnames_c = _pvnames_cv[:]
        plane = 'y'
    elif ctype.lower() == 'hv' or ctype.lower() == 'hv_f':
        pvnames_bpm = []
        pvnames_bpm.extend(_pvnames_bpm_x)
        pvnames_bpm.extend(_pvnames_bpm_y)
        pvnames_c = []
        pvnames_c.extend(_pvnames_ch)
        pvnames_c.extend(_pvnames_cv)
        plane = 'xy'
    kick0 = get_kick(ctype)
    respm = _np.empty((len(pvnames_bpm), len(pvnames_c)+1))
    old_orbit = _np.array(get_orbit(plane))
    for i, pvname in enumerate(pvnames_c):
        _pvs[pvname].value = kick0[i] + delta_kick/2.0
        p_orbit = _meas_new_orbit(old_orbit, plane)
        _pvs[pvname].value = kick0[i] - delta_kick/2.0
        n_orbit = _meas_new_orbit(p_orbit, plane)
        _pvs[pvname].value = kick0[i]
        old_orbit = _meas_new_orbit(n_orbit, plane)
        respm[:,i] = (p_orbit-n_orbit)/delta_kick
    if ctype.lower() == 'h_f' or ctype.lower() == 'v_f' or ctype.lower() == 'hv_f':
        delta_freq = 100.0
        freq0_RF = _pvs[PV_RF_FREQUENCY].value
        _pvs[PV_RF_FREQUENCY].value = freq0_RF + delta_freq/2.0
        p_orbit = _meas_new_orbit(old_orbit, plane)
        _pvs[PV_RF_FREQUENCY].value = freq0_RF - delta_freq/2.0
        n_orbit = _meas_new_orbit(p_orbit, plane)
        _pvs[PV_RF_FREQUENCY].value = freq0_RF
        old_orbit = _meas_new_orbit(n_orbit, plane)
        respm[:,-1] = (p_orbit-n_orbit)/delta_freq
    else:
        respm = _np.delete(respm, -1, axis=1)
    return respm
