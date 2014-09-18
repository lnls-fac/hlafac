#!/usr/bin/env/python3

import unittest
import numpy
import elements


DRIFT_TYPE = 'drift'
QUADRUPOLE_TYPE = 'quadrupole'


class TestElements(unittest.TestCase):

    def setUp(self):
        self.d_name = 'D1'
        self.d_length = 1.5
        self.q_name = 'Q1'
        self.q_k = 0.5
        self.drift = elements.Drift(
            name=self.d_name,
            length=self.d_length)
        self.quadrupole = elements.Quadrupole(
            name=self.q_name,
            k=self.q_k)

    def test_drift_name(self):
        self.assertEqual(self.drift.name, self.d_name,
                         msg='drift name wrong')

    def test_drift_type(self):
        self.assertEqual(self.drift.elem_type, DRIFT_TYPE,
                         msg='drift type wrong')

    def test_drift_matrix(self):
        drift_matrix = numpy.array([[1.0, self.d_length], [0.0, 1.0]])
        equal = numpy.equal(self.drift.matrix, drift_matrix)
        self.assertTrue(numpy.all(equal), msg='drift matrix wrong')

    def test_drift_get_length(self):
        self.assertEqual(self.drift.length, self.d_length,
                         msg='drift length wrong')

    def test_drift_set_length(self):
        new_length = 2.0
        self.drift.length = new_length
        drift_matrix = numpy.array([[1.0, new_length], [0.0, 1.0]])
        equal = numpy.equal(self.drift.matrix, drift_matrix)
        self.assertTrue(numpy.all(equal), msg='drift matrix wrong')

    def test_quadrupole_name(self):
        self.assertEqual(self.quadrupole.name, self.q_name,
                         msg='quadrupole name wrong')

    def test_quadrupole_type(self):
        self.assertEqual(self.quadrupole.elem_type, QUADRUPOLE_TYPE,
                         msg='quadrupole type wrong')

    def test_quadrupole_matrix(self):
        quadrupole_matrix = numpy.array([[1.0, 0.0], [self.q_k, 1.0]])
        equal = numpy.equal(self.quadrupole.matrix, quadrupole_matrix)
        self.assertTrue(numpy.all(equal), msg='quadrupole matrix wrong')

    def test_quadrupole_get_k(self):
        self.assertEqual(self.quadrupole.k, self.q_k,
                         msg='quadrupole k wrong')

    def test_quadrupole_set_k(self):
        new_k = 1.1
        self.quadrupole.k = new_k
        quadrupole_matrix = numpy.array([[1.0, 0.0], [new_k, 1.0]])
        equal = numpy.equal(self.quadrupole.matrix, quadrupole_matrix)
        self.assertTrue(numpy.all(equal), msg='quadrupole matrix wrong')

def elements_suite():
   suite = unittest.TestLoader().loadTestsFromTestCase(TestElements)
   return suite


def suite():
    suite_list = []
    suite_list.append(elements_suite())
    return unittest.TestSuite(suite_list)
