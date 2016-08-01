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

_reforbit_x_path = './reforbit_x/'
_reforbit_y_path = './reforbit_y/'
_reforbit_filetype = '.txt'
_reforbit_x_sel = 0
_reforbit_y_sel = 0
_reforbit_nslots = 3
_reforbit_x_data = None
_reforbit_y_data = None

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
    global _reforbit_xy, _reforbit_x, _reforbit_y
    _reforbit_xy = _np.empty((len(_api_pv._pvnames_bpm_x)+len(_api_pv._pvnames_bpm_y)))
    if plane.lower() == 'x':
        _reforbit_x = _reforbit_x_data[:,_reforbit_x_sel]
        _reforbit_xy[:len(_reforbit_x)] = _reforbit_x
    elif plane.lower() == 'y':
        _reforbit_y = _reforbit_y_data[:,_reforbit_y_sel]
        _reforbit_xy[-len(_reforbit_y):] = _reforbit_y


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
        reforbit = _reforbit_x
    elif plane.lower() == 'y':
        reforbit = _reforbit_y
    return reforbit


def set_respm():
    global _respm_h, _respm_v, _respm_hv, _respm_h_v, _respm_h_f, _respm_v_f, _respm_hv_f, _respm_h_v_f

    _respm_hv_f = _respm_data[:,:,_respm_sel]
    _respm_hv = _respm_hv_f[:,:-1]
    _respm_h = _respm_hv[:len(_api_pv._pvnames_bpm_x),:len(_api_pv._pvnames_ch)]
    _respm_v = _respm_hv[len(_api_pv._pvnames_bpm_x):,len(_api_pv._pvnames_ch):]
    _respm_h_v_f = _respm_hv_f[:]
    _respm_h_v_f[:len(_api_pv._pvnames_bpm_x),len(_api_pv._pvnames_ch):-1] = _np.zeros(_respm_v.shape)
    _respm_h_v_f[len(_api_pv._pvnames_bpm_x):,:len(_api_pv._pvnames_ch)] = _np.zeros(_respm_h.shape)
    _respm_h_v = _respm_h_v_f[:,:-1]
    _respm_h_f = _respm_h[:]
    _np.c_[_respm_h_f,_respm_hv_f[:len(_api_pv._pvnames_bpm_x),-1]]
    _respm_v_f = _respm_v[:]
    _np.c_[_respm_v_f,_respm_hv_f[len(_api_pv._pvnames_bpm_x):,-1]]


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
    respm = _respm_hv_f
    return respm


def calc_kick(orbit = None, ctype = ''):
    kick, reforbit, inv_respm = None, None, None
    if ctype.lower() == 'h':
        reforbit = _reforbit_x
        inv_respm = _inv_respm_h
    elif ctype.lower() == 'v':
        reforbit = _reforbit_y
        inv_respm = _inv_respm_v
    elif ctype.lower() == 'hv':
        reforbit = _reforbit_xy
        inv_respm = _inv_respm_hv
    elif ctype.lower() == 'h_v':
        reforbit = _reforbit_xy
        inv_respm = _inv_respm_h_v
    elif ctype.lower() == 'h_f':
        reforbit = _reforbit_x
        inv_respm = _inv_respm_h_f
    elif ctype.lower() == 'v_f':
        reforbit = _reforbit_y
        inv_respm = _inv_respm_v_f
    elif ctype.lower() == 'hv_f':
        reforbit = _reforbit_xy
        inv_respm = _inv_respm_hv_f
    elif ctype.lower() == 'h_v_f':
        reforbit = _reforbit_xy
        inv_respm = _inv_respm_h_v_f
    if reforbit is not None and inv_respm is not None:
        kick = _np.dot(inv_respm,(reforbit-orbit))
    return kick


def _load(fname):
    return _np.loadtxt(fname)


def _save(fname, var):
    _np.savetxt(fname, var, delimiter = ' ')


def _calculate_inv_respm(respm = None):
    U, s, V = _np.linalg.svd(respm, full_matrices = False)
    S = _np.diag(s)
    inv_respm = _np.dot(_np.dot(_np.transpose(V),_np.linalg.pinv(S)),_np.transpose(U))
    return inv_respm
