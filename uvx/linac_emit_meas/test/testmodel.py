#!/usr/bin/env python3

import unittest
import numpy
import model
import testlinac


class TestEmptyModel(unittest.TestCase):

    def test_empty(self):
        self.model = model.Model()
        self.assertEqual(len(self.model.elements), 0,
                         msg='model not empty')


class TestLinacModel(unittest.TestCase):

    def setUp(self):
        self.model = model.Model(testlinac.element_list())

    def test_num_elements(self):
        self.assertEqual(len(self.model.elements), 2,
                         msg='wrong number of elements in model')

    def test_first_element_name(self):
        self.assertEqual(self.model.elements[0].name, 'Q1',
                         msg='wrong name for first model element')

    def test_second_element_name(self):
        self.assertEqual(self.model.elements[1].name, 'D1',
                         msg='wrong name for first model element')

    def test_matrix(self):
        matrix = numpy.array([[1.75, 2.5], [0.3, 1.0]])
        equal = numpy.equal(matrix, self.model.matrix())
        self.assertTrue(numpy.all(equal),
                        msg='wrong matrix in model')


class TestException(unittest.TestCase):

    def test_element_list_exception(self):
        kwargs = {'element_list': [0, 1]}
        self.assertRaises(TypeError, model.Model, **kwargs)


def empty_model_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEmptyModel)
    return suite


def linac_model_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLinacModel)
    return suite


def exception_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestException)
    return suite


def suite():
    suite_list = []
    suite_list.append(empty_model_suite())
    suite_list.append(linac_model_suite())
    suite_list.append(exception_suite())
    return unittest.TestSuite(suite_list)
