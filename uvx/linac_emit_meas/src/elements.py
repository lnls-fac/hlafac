#!/usr/bin/env python3

import numpy


class Element(object):

    def __init__(self, name, elem_type):
        self.name = name
        self.elem_type = elem_type


class Drift(Element):

    def __init__(self, name, length):
        super().__init__(name=name, elem_type='drift')
        self.matrix = numpy.array([[1.0, length], [0.0, 1.0]])

    @property
    def length(self):
        return self.matrix[0, 1]

    @length.setter
    def length(self, value):
        self.matrix[0, 1] = value


class Quadrupole(Element):

    def __init__(self, name, k):
        super().__init__(name=name, elem_type='quadrupole')
        self.matrix = numpy.array([[1.0, 0.0], [k, 1.0]])

    @property
    def k(self):
        return self.matrix[1, 0]

    @k.setter
    def k(self, value):
        self.matrix[1, 0] = value
