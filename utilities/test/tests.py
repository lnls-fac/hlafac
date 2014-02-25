"""Tests for utils package"""

import unittest
import test_timer


suite_list = []
suite_list.append(test_timer.suite())

tests = unittest.TestSuite(suite_list)
unittest.TextTestRunner(verbosity=2).run(tests)
