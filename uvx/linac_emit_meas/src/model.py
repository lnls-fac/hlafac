#!/usr/bin/env python3

import numpy
import elements


class Model(object):

    def __init__(self, element_list=None):
        if element_list is not None:
            self._check_element_list(element_list)
            self.elements = element_list
        else:
            self.elements = []

    def matrix(self):
        m = numpy.eye(2)
        for element in self.elements:
            m = element.matrix.dot(m)
        return m

    def _check_element_list(self, element_list):
        for element in element_list:
            if not isinstance(element, elements.Element):
                raise TypeError('Invalid element in list')
