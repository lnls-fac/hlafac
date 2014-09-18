#!/usr/bin/env python3

import copy
import numpy
import numpy.linalg


NUM_ITERS = 100


def calc_emit(model, quadrupole_idx, k, measured_beam_size, size_error=None):

    emit, sigma_0 = calc_emit_from_beam_size(
        model,
        quadrupole_idx,
        k,
        measured_beam_size)

    if size_error is not None:
        emit_with_errors = []
        for i in range(NUM_ITERS):
            beam_size_with_errors = propagate_beam_size(
                sigma_0,
                model,
                quadrupole_idx,
                k,
                size_error)
            new_emit, new_sigma_0 = calc_emit_from_beam_size(
                model,
                quadrupole_idx,
                k,
                beam_size_with_errors)
            emit_with_errors.append(new_emit)
        emit_error = numpy.std(emit_with_errors)
    else:
        emit_error = None

    return emit, emit_error


def calc_emit_from_beam_size(model, quadrupole_idx, k, beam_size):
    sigma_out_11 = numpy.power(beam_size, 2)
    sigma_0 = calc_sigma_0(model, quadrupole_idx, k, sigma_out_11)
    emit = numpy.sqrt(numpy.linalg.det(sigma_0))

    return emit, sigma_0


def calc_sigma_0(model, quadrupole_idx, k, sigma_out_11):
    r = []
    for x in k:
        model.elements[quadrupole_idx].k = x
        matrix = model.matrix()
        r_1 = matrix[0, 0]**2
        r_2 = 2*matrix[0, 0]*matrix[0, 1]
        r_3 = matrix[0, 1]**2
        r.append([r_1, r_2, r_3])
    r = numpy.array(r)

    u, s, v = numpy.linalg.svd(r, full_matrices=False)

    r_inv = v.transpose().dot(numpy.diag(1/s)).dot(u.transpose())
    sigma_vec = r_inv.dot(sigma_out_11)

    sigma_0 = numpy.array([[sigma_vec[0], sigma_vec[1]],
                           [sigma_vec[1], sigma_vec[2]]])

    return sigma_0


def propagate_beam_size(sigma_0, model, quadrupole_idx, k, size_error=0.0):
    new_model = copy.deepcopy(model)
    beam_size = []
    for x in k:
        quadrupole = new_model.elements[quadrupole_idx].k = x
        r = new_model.matrix()
        sigma_out = r.dot(sigma_0).dot(r.transpose())
        beam_size.append(numpy.sqrt(sigma_out[0, 0]))
    beam_size = numpy.array(beam_size)

    if size_error > 0.0:
        beam_size += numpy.random.normal(size=len(k), scale=size_error)

    return beam_size
