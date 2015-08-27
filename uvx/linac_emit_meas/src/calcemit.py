#!/usr/bin/env python3

import copy as _copy
import numpy as _numpy


_DEFAULT_NUM_SAMPLES = 100


def calc_emit(model, quadrupole_idx, k, measured_beam_size, short=True, 
        size_error=None, num_samples=_DEFAULT_NUM_SAMPLES):
    """Calculate beam emittance and rms error estimate from quadrupole and
    measured beam size values.
    
    Arguments:
    model -- line model as list of elements
    quadrupole_idx -- index of quadrupole used in measurement in model
    k -- vector of quadrupole values
    measured_beam_size -- vector of beam sizes for each value of k
    short -- if True, model matrix elements are summed in calculation of
        initial beam matrix (default True)
    size_error -- error in beam_size (optional)
    num_samples -- number of sample experiments to simulate for estimating the
        calculated emittance error if size_error is given (default 100)
    
    Return values:
    emit -- calculated beam emittance
    emit_error -- None, if no size_error is supplied; standard deviation of
        simulated experiment emittances otherwise
    """

    emit, sigma_0 = _calc_emit_from_beam_size(model, quadrupole_idx, k,
                                              measured_beam_size, short)

    if size_error is not None:
        emit_error = _calc_emit_error(model, quadrupole_idx, k, size_error,
                                      sigma_0, num_samples, short)
    else:
        emit_error = None

    return emit, emit_error


def _calc_emit_error(model, quadrupole_idx, k, size_error, sigma_0,
                     num_samples, short):
    emit_with_errors = []
    for i in range(num_samples):
        size_with_errors = propagate_beam_size(
            sigma_0, model, quadrupole_idx,
            k, size_error)
        emit, new_sigma = _calc_emit_from_beam_size(
            model, quadrupole_idx, k,
            size_with_errors, short)
        emit_with_errors.append(emit)

    emit_error = _numpy.std(emit_with_errors)
    return emit_error


def propagate_beam_size(sigma_0, model, quadrupole_idx, k, size_error=0.0):
    """Propagate beam matrix by model for different values of quadrupole.
    
    Arguments:
    sigma_0 -- initial beam matrix
    model -- line model as list of elements
    quadrupole_idx -- index of quadrupole used in measurement in model

    """
    new_model = _copy.deepcopy(model)
    beam_size = []
    for x in k:
        quadrupole = new_model.elements[quadrupole_idx].k = x
        r = new_model.matrix()
        sigma_out = r.dot(sigma_0).dot(r.transpose())
        beam_size.append(_numpy.sqrt(sigma_out[0, 0]))
    beam_size = _numpy.array(beam_size)

    if size_error > 0.0:
        beam_size += _numpy.random.normal(size=len(k), scale=size_error)

    return beam_size


def _calc_emit_from_beam_size(model, quadrupole_idx, k, beam_size, short):
    sigma_out_11 = _numpy.power(beam_size, 2)
    sigma_0 = _calc_sigma_0(model, quadrupole_idx, k, sigma_out_11, short)
    emit = _numpy.sqrt(_numpy.linalg.det(sigma_0))

    return emit, sigma_0


def _calc_sigma_0(model, quadrupole_idx, k, sigma_out_11, short):
    r = []
    for x in k:
        model.elements[quadrupole_idx].k = x
        matrix = model.matrix()
        r_1 = matrix[0, 0]**2
        r_2 = 2*matrix[0, 0]*matrix[0, 1]
        r_3 = matrix[0, 1]**2
        r.append([r_1, r_2, r_3])
    r = _numpy.array(r)

    if short:
        sigma_0 = _calc_sigma_0_with_sum(r, sigma_out_11)
    else:
        sigma_0 = _calc_sigma_0_without_sum(r, sigma_out_11)

    return sigma_0
    

def _calc_sigma_0_with_sum(r, sigma_out_11):
    a = r.transpose().dot(r)
    b = _numpy.array([sum(r[:, 0]*sigma_out_11),
                      sum(r[:, 1]*sigma_out_11),
                      sum(r[:, 2]*sigma_out_11)])

    sigma_vec = _numpy.linalg.solve(a, b)

    sigma_0 = _build_sigma_matrix(sigma_vec)
    return sigma_0


def _calc_sigma_0_without_sum(r, sigma_out_11):
    u, s, v = _numpy.linalg.svd(r, full_matrices=False)
    
    u_inv = u.transpose()
    s_inv = _numpy.diag(1/s)
    v_inv = v.transpose()

    r_inv = v_inv.dot(s_inv).dot(u_inv)
    sigma_vec = r_inv.dot(sigma_out_11)

    sigma_0 = _build_sigma_matrix(sigma_vec)
    return sigma_0


def _build_sigma_matrix(sigma_vec):
    return _numpy.array([[sigma_vec[0], sigma_vec[1]],
                         [sigma_vec[1], sigma_vec[2]]])
