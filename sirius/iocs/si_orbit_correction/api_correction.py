import numpy as _np
from scipy import io as _io
import epics as _epics
import sirius as _sirius
import api_pv as _api_pv
from time import sleep


_respm_path = './respm/'
_respm_filetype = '.txt'
_respm_sel = 0
_respm_nslots = 3
_respm_data = None
_respm_full = None

_reforbit_x_path = './reforbit_x/'
_reforbit_y_path = './reforbit_y/'
_reforbit_filetype = '.txt'
_reforbit_x_sel = 0
_reforbit_y_sel = 0
_reforbit_nslots = 3
_reforbit_x_data = None
_reforbit_y_data = None
_reforbit_x_full = None
_reforbit_y_full = None

_model = None
_respm_hv = None
_respm_h = None
_respm_v = None
_respm_h_v = None
_inv_respm_hv = None
_inv_respm_h = None
_inv_respm_v = None
_inv_respm_h_v = None
_respm_hv_f = None
_respm_h_f = None
_respm_v_f = None
_respm_h_v_f = None
_inv_respm_hv_f = None
_inv_respm_h_f = None
_inv_respm_v_f = None
_inv_respm_h_v_f = None
_reforbit_xy = None
_reforbit_x = None
_reforbit_y = None

_bpm_sel = None
_ch_sel = None
_cv_sel = None
_idx_bpm_x_y = None
_idx_bpm = None
_idx_ch = None
_idx_cv = None
_idx_c = None


def initialize_slot(var_type = None, slot = None):
    global _reforbit_x_data, _reforbit_y_data, _respm_data
    if slot == None:
        if var_type.lower() == 'reforbit_x':
            _reforbit_x_data = _np.empty((len(_api_pv._pvnames_bpm_x), _reforbit_nslots))
            for i in range(_reforbit_nslots):
                _reforbit_x_data[:,i] = _load(_reforbit_x_path + str(i) + _reforbit_filetype)
        elif var_type.lower() == 'reforbit_y':
            _reforbit_y_data = _np.empty((len(_api_pv._pvnames_bpm_y), _reforbit_nslots))
            for i in range(_reforbit_nslots):
                _reforbit_y_data[:,i] = _load(_reforbit_y_path + str(i) + _reforbit_filetype)
        elif var_type.lower() == 'respm':
            _respm_data = _np.empty((len(_api_pv._pvnames_bpm_x)+len(_api_pv._pvnames_bpm_y), len(_api_pv._pvnames_ch)+len(_api_pv._pvnames_cv)+1, _respm_nslots))
            for i in range(_respm_nslots):
                _respm_data[:,:,i] = _load(_respm_path + str(i) + _respm_filetype)
        elif var_type.lower() == 'all':
            initialize_slot('reforbit_x')
            initialize_slot('reforbit_y')
            initialize_slot('respm')
    else:
        if var_type.lower() == 'reforbit_x':
            _reforbit_x_data[:,slot] = _load(_reforbit_x_path + str(slot) + _reforbit_filetype)
        elif var_type.lower() == 'reforbit_y':
            _reforbit_y_data[:,slot] = _load(_reforbit_y_path + str(slot) + _reforbit_filetype)
        elif var_type.lower() == 'respm':
            _respm_data[:,:,slot] = _load(_respm_path + str(slot) + _respm_filetype)


def set_reforbit(plane = ''):
    global _reforbit_x_full, _reforbit_y_full, _reforbit_xy, _reforbit_x, _reforbit_y
    _reforbit_xy = _np.empty((len(_idx_bpm)))
    if plane.lower() == 'x':
        _reforbit_x_full  = _reforbit_x_data[:,_reforbit_x_sel]
        _reforbit_x = _reforbit_x_full[_idx_bpm_x_y]
        _reforbit_xy[:len(_reforbit_x)] = _reforbit_x
    elif plane.lower() == 'y':
        _reforbit_y_full = _reforbit_y_data[:,_reforbit_y_sel]
        _reforbit_y = _reforbit_y_full[_idx_bpm_x_y]
        _reforbit_xy[-len(_reforbit_y):] = _reforbit_y
    elif plane.lower() == 'xy':
        set_reforbit('x')
        set_reforbit('y')


def set_reforbit_slot(slot = None, plane = ''):
    global _reforbit_x_sel, _reforbit_y_sel
    if plane.lower() == 'x': _reforbit_x_sel = slot
    elif plane.lower() == 'y': _reforbit_y_sel = slot


def update_reforbit_slot(reforbit = None, plane = ''):
    if plane.lower() == 'x':
        _save(_reforbit_x_path + str(_reforbit_x_sel) + _reforbit_filetype, reforbit)
        initialize_slot('reforbit_x', _reforbit_x_sel)
    elif plane.lower() == 'y':
        _save(_reforbit_y_path + str(_reforbit_y_sel) + _reforbit_filetype, reforbit)
        initialize_slot('reforbit_y', _reforbit_y_sel)


def get_reforbit(plane = ''):
    if plane.lower() == 'x':
        return _reforbit_x_full
    elif plane.lower() == 'y':
        return _reforbit_y_full


def set_respm():
    global _respm_full, _respm_h, _respm_v, _respm_hv, _respm_h_v, _respm_h_f, _respm_v_f, _respm_hv_f, _respm_h_v_f

    _respm_full = _respm_data[:,:,_respm_sel]
    _respm_hv_f = _np.copy(_respm_full[_idx_bpm,:][:,_idx_c])
    _respm_hv = _np.copy(_respm_hv_f[:,:-1])
    _respm_h = _np.copy(_respm_hv[:len(_idx_bpm_x_y),:len(_idx_ch)])
    _respm_v = _np.copy(_respm_hv[-len(_idx_bpm_x_y):,-len(_idx_cv):])
    _respm_h_v_f = _np.copy(_respm_hv_f)
    _respm_h_v_f[:len(_idx_bpm_x_y),len(_idx_ch):-1] = _np.zeros((_respm_v.shape))
    _respm_h_v_f[-len(_idx_bpm_x_y):,:len(_idx_ch)] = _np.zeros(_respm_h.shape)
    _respm_h_v = _np.copy(_respm_h_v_f[:,:-1])
    _respm_h_f = _np.copy(_respm_h)
    _respm_h_f = _np.c_[_respm_h_f,_respm_hv_f[:len(_idx_bpm_x_y),-1]]
    _respm_v_f = _np.copy(_respm_v)
    _respm_v_f = _np.c_[_respm_v_f,_respm_hv_f[-len(_idx_bpm_x_y):,-1]]


def set_inv_respm():
    global _inv_respm_h, _inv_respm_v, _inv_respm_hv, _inv_respm_h_v, _inv_respm_h_f, _inv_respm_v_f, _inv_respm_hv_f, _inv_respm_h_v_f
    if (_respm_hv_f != []) and (_respm_hv_f is not None):
        _inv_respm_hv = _calculate_inv_respm(_respm_hv)
        _inv_respm_h = _calculate_inv_respm(_respm_h)
        _inv_respm_v = _calculate_inv_respm(_respm_v)
        _inv_respm_h_v = _calculate_inv_respm(_respm_h_v)
        _inv_respm_hv_f = _calculate_inv_respm(_respm_hv_f)
        _inv_respm_h_f = _calculate_inv_respm(_respm_h_f)
        _inv_respm_v_f = _calculate_inv_respm(_respm_v_f)
        _inv_respm_h_v_f = _calculate_inv_respm(_respm_h_v_f)


def set_respm_slot(slot = None):
    global _respm_sel
    _respm_sel = slot


def update_respm_slot(respm_array = None, reshape = False):
    if reshape:
        respm = _np.reshape(respm_array, (len(_api_pv._pvnames_bpm_x)+len(_api_pv._pvnames_bpm_y), len(_api_pv._pvnames_ch)+len(_api_pv._pvnames_cv)+1), order='F')
    else:
        respm = respm_array
    _save(_respm_path + str(_respm_sel) + _respm_filetype, respm)
    initialize_slot('respm', _respm_sel)


def get_respm():
    return _respm_full


def initialize_device_sel():
    global _bpm_sel, _ch_sel, _cv_sel
    _bpm_sel = _np.ones(len(_api_pv._pvnames_bpm_x))
    _ch_sel = _np.ones(len(_api_pv._pvnames_ch))
    _cv_sel = _np.ones(len(_api_pv._pvnames_cv))


def update_device_sel(device = '', device_sel = None):
    global _bpm_sel, _ch_sel, _cv_sel
    if device.lower() == 'bpm':
        _bpm_sel = _np.array(device_sel)
    elif device.lower() == 'ch':
        _ch_sel = _np.array(device_sel)
    elif device.lower() == 'cv':
        _cv_sel = _np.array(device_sel)


def set_device_sel(device = ''):
    global _idx_bpm_x_y, _idx_bpm, _idx_ch, _idx_cv, _idx_c
    if device.lower() == 'bpm':
        _idx_bpm_x_y = _np.where(_bpm_sel)[0]
        _idx_bpm = _np.where(_np.concatenate((_bpm_sel,_bpm_sel),axis=0))[0]
    elif device.lower() == 'ch':
        _idx_ch = _np.where(_ch_sel)[0]
        _idx_c = _np.where(_np.concatenate((_ch_sel,_cv_sel,[1]),axis=0))[0]
    elif device.lower() == 'cv':
        _idx_cv = _np.where(_cv_sel)[0]
        _idx_c = _np.where(_np.concatenate((_ch_sel,_cv_sel,[1]),axis=0))[0]
    elif device.lower() == 'all':
        set_device_sel('bpm')
        set_device_sel('ch')
        set_device_sel('cv')


def get_device_sel(device = ''):
    if device.lower() == 'bpm':
        return _bpm_sel
    elif device.lower() == 'ch':
        return _ch_sel
    elif device.lower() == 'cv':
        return _cv_sel


def change_device_status(device = '', devicename = '', status = None):
    global _bpm_sel, _ch_sel, _cv_sel
    if device.lower() == 'bpm':
        idx = _api_pv._devicenames_bpm.index(devicename)
        _bpm_sel[idx] = status
    elif device.lower() == 'ch':
        idx = _api_pv._devicenames_ch.index(devicename)
        _ch_sel[idx] = status
    elif device.lower() == 'cv':
        idx = _api_pv._devicenames_cv.index(devicename)
        _cv_sel[idx] = status


def calc_kick(orbit_full = None, ctype = ''):
    kick, reforbit, inv_respm = None, None, None
    if ctype.lower() == 'h' or ctype.lower() == 'v' or ctype.lower() == 'h_f' or ctype.lower() == 'v_f':
        orbit = orbit_full[_idx_bpm_x_y]
        if ctype.lower() == 'h':
            reforbit = _reforbit_x
            inv_respm = _inv_respm_h
        elif ctype.lower() == 'v':
            reforbit = _reforbit_y
            inv_respm = _inv_respm_v
        elif ctype.lower() == 'h_f':
            reforbit = _reforbit_x
            inv_respm = _inv_respm_h_f
        elif ctype.lower() == 'v_f':
            reforbit = _reforbit_y
            inv_respm = _inv_respm_v_f
    elif ctype.lower() == 'h_v' or ctype.lower() == 'hv' or ctype.lower() == 'h_v_f' or ctype.lower() == 'hv_f':
        orbit = orbit_full[_idx_bpm]
        if ctype.lower() == 'hv':
            reforbit = _reforbit_xy
            inv_respm = _inv_respm_hv
        elif ctype.lower() == 'h_v':
            reforbit = _reforbit_xy
            inv_respm = _inv_respm_h_v
        elif ctype.lower() == 'hv_f':
            reforbit = _reforbit_xy
            inv_respm = _inv_respm_hv_f
        elif ctype.lower() == 'h_v_f':
            reforbit = _reforbit_xy
            inv_respm = _inv_respm_h_v_f
    if reforbit is not None and inv_respm is not None:
        kick = _np.dot(-inv_respm,(reforbit-orbit))
    return kick


def _load(fname):
    return _np.loadtxt(fname, delimiter=' ')


def _save(fname, var):
    _np.savetxt(fname, var, fmt='%+.8e', delimiter = ' ')


def _calculate_inv_respm(respm = None):
    U, s, V = _np.linalg.svd(respm, full_matrices = False)
    S = _np.diag(s)
    inv_respm = _np.dot(_np.dot(_np.transpose(V),_np.linalg.pinv(S)),_np.transpose(U))
    return inv_respm
