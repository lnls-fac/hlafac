"""
Tests
    Test CustomPlot project.

Afonso Haruo Carnielli Mukai (FAC - LNLS)

2013-11-21: v0.1
"""

import unittest
import Test_ColorConversion
import Test_CustomPlot
import Test_DateTimePlot
import Test_PositionPlot
import Test_DateTimeLine

suite_list = []
suite_list.append(Test_CustomPlot.suite())
suite_list.append(Test_ColorConversion.suite())
suite_list.append(Test_DateTimePlot.suite())
suite_list.append(Test_PositionPlot.suite())
suite_list.append(Test_DateTimeLine.suite())

tests = unittest.TestSuite(suite_list)
unittest.TextTestRunner(verbosity=2).run(tests)
