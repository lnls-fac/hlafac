#!/usr/bin/env python3

import unittest
import testcalcemit
import testelements
import testmodel


suite_list = []
suite_list.append(testcalcemit.suite())
suite_list.append(testelements.suite())
suite_list.append(testmodel.suite())

tests = unittest.TestSuite(suite_list)
unittest.TextTestRunner(verbosity=2).run(tests)
