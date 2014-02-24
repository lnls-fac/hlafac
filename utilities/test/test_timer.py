"""Tests for self.timer module."""

import threading
import unittest
import utils.timer


class TestTimer(unittest.TestCase):
    def setUp(self):
        self.counter = 0
        self.list = []
        self.event = threading.Event()
        
    def test_start_and_stop_before_function_is_called(self):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function)
        self._start_wait_and_stop_timer(0.00)
        self.assertEqual(self.counter, 0, 'function was called')
    
    def test_start_and_stop_twice(self):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function)
        self._start_wait_and_stop_timer(0.06)
        self._start_wait_and_stop_timer(0.11)
        self.assertEqual(self.counter, 3,
                         'function was not called right number of times')
    
    def test_call_function_twice(self):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function)
        self._start_wait_and_stop_timer(0.11)
        self.assertEqual(self.counter, 2,
                         'function was not called right number of times')
    
    def test_call_function_with_no_arguments(self):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function)
        self._start_wait_and_stop_timer(0.06)
        self.assertTrue(len(self.list)==0, 'list not empty')
    
    def test_call_function_with_tuple(self):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function,
                                  args=(1, 2))
        self._start_wait_and_stop_timer(0.06)
        self.assertEqual(self.list, [1, 2], 'lists differ')
    
    def test_call_function_with_dict(self):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function,
                                  kwargs={'a': 4, 'b': 3})
        self._start_wait_and_stop_timer(0.06)
        self.assertEqual(self.list, [4, 3], 'lists differ')

    def test_call_function_with_tuple_and_dict(self):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function,
                                  args=(5,), kwargs={'b': 6})
        self._start_wait_and_stop_timer(0.06)
        self.assertEqual(self.list, [5, 6], 'lists differ')
    
    def _function(self, a=None, b=None):
        if a is not None:
            self.list.append(a)
        if b is not None:
            self.list.append(b)
        self.counter += 1
    
    def _start_wait_and_stop_timer(self, timeout):
        self.timer.start()
        self.event.wait(timeout)
        self.timer.stop()
