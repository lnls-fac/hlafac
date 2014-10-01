#!/usr/bin/env python3

import unittest
import numpy
import calcemit
import model
import testlinac


class TestCalcEmit(unittest.TestCase):

    def setUp(self):
        sigma_11 = 40e-9
        sigma_12 = 5e-9
        sigma_22 = 60e-9

        sigma_0 = numpy.array([[sigma_11, sigma_12], [sigma_12, sigma_22]])
        self.emit = numpy.sqrt(numpy.linalg.det(sigma_0))

        self.k = numpy.linspace(-0.8, -0.3, 50)

        self.m = model.Model(testlinac.element_list())
        self.q_idx = 0

        self.measured_beam_size = calcemit.propagate_beam_size(
            sigma_0=sigma_0,
            model=self.m,
            quadrupole_idx=self.q_idx,
            k=self.k)

    def test_calc_emit_without_error(self):
        calculated_emit, emit_error = calcemit.calc_emit(
            model=self.m,
            quadrupole_idx=self.q_idx,
            k=self.k,
            measured_beam_size=self.measured_beam_size)
        self.assertAlmostEqual(calculated_emit, self.emit, places=11,
                               msg="wrong value for calculated emittance")
        
    def test_calc_emit_with_error_and_sum(self):
        calculated_emit, emit_error = calcemit.calc_emit(
            model=self.m,
            quadrupole_idx=self.q_idx,
            k=self.k,
            measured_beam_size=self.measured_beam_size,
            size_error=0.01*max(self.measured_beam_size),
            num_samples=100)
        self.assertAlmostEqual(calculated_emit, self.emit, places=11,
                               msg="wrong value for calculated emittance")

    def test_calc_emit_with_error_without_sum(self):
        calculated_emit, emit_error = calcemit.calc_emit(
            model=self.m,
            quadrupole_idx=self.q_idx,
            k=self.k,
            measured_beam_size=self.measured_beam_size,
            size_error=0.01*max(self.measured_beam_size),
            num_samples=100,
            short=False)
        self.assertAlmostEqual(calculated_emit, self.emit, places=11,
                               msg="wrong value for calculated emittance")


def calc_emit_suite():
     suite = unittest.TestLoader().loadTestsFromTestCase(TestCalcEmit)
     return suite


def suite():
    suite_list = []
    suite_list.append(calc_emit_suite())
    return unittest.TestSuite(suite_list)
