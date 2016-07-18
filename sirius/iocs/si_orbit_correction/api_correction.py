import numpy as _np
from scipy import io as _io
import epics as _epics
import sirius as _sirius
import api_pv as _api_pv
from time import sleep


respm_path = './respm/'
respm_filetype = '.txt'

_model = None
_respm_hv = None
_respm_h = None
_respm_v = None
_respm_h_v = None
_inv_respm_hv = None
_inv_respm_h = None
_inv_respm_v = None
_inv_respm_h_v = None
_respm_hv_f = 'respm_hv_f_va'
_respm_h_f = None
_respm_v_f = None
_respm_h_v_f = None
_inv_respm_hv_f = None
_inv_respm_h_f = None
_inv_respm_v_f = None
_inv_respm_h_v_f = None
_reference_orbit_xy = _np.zeros(2*len(_api_pv._pvnames_bpm_x))
_reference_orbit_x = None
_reference_orbit_y = None


def set_reference_orbit(reference_orbit = None, plane = ''):
    global _reference_orbit_xy, _reference_orbit_x, _reference_orbit_y
    if plane.lower() == 'x':
        if reference_orbit is not None:
            _reference_orbit_x = reference_orbit
        else:
            _reference_orbit_x = _np.zeros(len(_api_pv._pvnames_bpm_x))
        _reference_orbit_xy[:len(_reference_orbit_xy)/2] = _reference_orbit_x
    elif plane.lower() == 'y':
        if reference_orbit is not None:
            _reference_orbit_y = reference_orbit
        else:
            _reference_orbit_y= _np.zeros(2*len(_api_pv._pvnames_bpm_y))
        _reference_orbit_xy[len(_reference_orbit_xy)/2:] = _reference_orbit_y
    elif plane.lower() == 'xy':
        if reference_orbit is not None:
            _reference_orbit_xy = reference_orbit
        else:
            _reference_orbit_xy[:] = _np.zeros(len(_reference_orbit_xy))
        _reference_orbit_x = _reference_orbit_xy[:len(_reference_orbit_xy)/2]
        _reference_orbit_y = _reference_orbit_xy[len(_reference_orbit_xy)/2:]


def set_respm(respm = None):
    global _respm_h, _respm_v, _respm_hv, _respm_h_v, _inv_respm_h, _inv_respm_v, _inv_respm_hv, _inv_respm_h_v, _respm_h_f, _respm_v_f, _respm_hv_f, _respm_h_v_f, _inv_respm_h_f, _inv_respm_v_f, _inv_respm_hv_f, _inv_respm_h_v_f
    if respm is None:
        _respm_hv_f = _api_pv.meas_respm('hv')
    else:
        _respm_hv_f = _np.loadtxt(respm_path + respm + respm_filetype)
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

    if (_respm_hv_f != []) and (_respm_hv_f is not None):
        _inv_respm_hv = _calculate_inv_respm(_respm_hv)
        _inv_respm_h = _calculate_inv_respm(_respm_h)
        _inv_respm_v = _calculate_inv_respm(_respm_v)
        _inv_respm_h_v = _calculate_inv_respm(_respm_h_v)
        _inv_respm_hv_f = _calculate_inv_respm(_respm_hv_f)
        _inv_respm_h_f = _calculate_inv_respm(_respm_h_f)
        _inv_respm_v_f = _calculate_inv_respm(_respm_v_f)
        _inv_respm_h_v_f = _calculate_inv_respm(_respm_h_v_f)


def calc_kick(orbit = None, ctype = ''):
    kick, reference_orbit, inv_respm = None, None, None
    if ctype.lower() == 'h':
        reference_orbit = _reference_orbit_x
        inv_respm = _inv_respm_h
    elif ctype.lower() == 'v':
        reference_orbit = _reference_orbit_y
        inv_respm = _inv_respm_v
    elif ctype.lower() == 'hv':
        reference_orbit = _reference_orbit_xy
        inv_respm = _inv_respm_hv
    elif ctype.lower() == 'h_v':
        reference_orbit = _reference_orbit_xy
        inv_respm = _inv_respm_h_v
    elif ctype.lower() == 'h_f':
        reference_orbit = _reference_orbit_x
        inv_respm = _inv_respm_h_f
    elif ctype.lower() == 'v_f':
        reference_orbit = _reference_orbit_y
        inv_respm = _inv_respm_v_f
    elif ctype.lower() == 'hv_f':
        reference_orbit = _reference_orbit_xy
        inv_respm = _inv_respm_hv_f
    elif ctype.lower() == 'h_v_f':
        reference_orbit = _reference_orbit_xy
        inv_respm = _inv_respm_h_v_f
    if reference_orbit is not None and inv_respm is not None:
        kick = _np.dot(inv_respm,(reference_orbit-orbit))
    return kick


def _calculate_inv_respm(respm = None):
    U, s, V = _np.linalg.svd(respm, full_matrices = False)
    S = _np.diag(s)
    inv_respm = _np.dot(_np.dot(_np.transpose(V),_np.linalg.pinv(S)),_np.transpose(U))
    return inv_respm
