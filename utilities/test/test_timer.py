"""Tests for timer module."""

import threading
import unittest
import utils.timer


class TestTimerFunction(unittest.TestCase):
    
    def setUp(self):
        self.counter = 0
        self.list = []
        self.event = threading.Event()
        
    def test_start_and_stop_before_function_is_called(self):
        self._create_timer()
        self._start_wait_and_stop_timer(0.00)
        self.assertEqual(self.counter, 0, 'function was called')
    
    def test_start_and_stop_twice(self):
        self._create_timer()
        self._start_wait_and_stop_timer(0.06)
        self._start_wait_and_stop_timer(0.11)
        self.assertEqual(self.counter, 3,
                         'function was not called right number of times')
    
    def test_call_function_twice(self):
        self._create_timer()
        self._start_wait_and_stop_timer(0.11)
        self.assertEqual(self.counter, 2,
                         'function was not called right number of times')
    
    def test_call_function_with_no_arguments(self):
        self._create_timer()
        self._start_wait_and_stop_timer(0.06)
        self.assertTrue(len(self.list)==0, 'list not empty')
    
    def test_call_function_with_tuple(self):
        self._create_timer(args=(1, 2))
        self._start_wait_and_stop_timer(0.06)
        self.assertEqual(self.list, [1, 2], '')
    
    def test_call_function_with_dict(self):
        self._create_timer(kwargs={'a': 4, 'b': 3})
        self._start_wait_and_stop_timer(0.06)
        self.assertEqual(self.list, [4, 3], 'lists differ')

    def test_call_function_with_tuple_and_dict(self):
        self._create_timer(args=(5,), kwargs={'b': 6})
        self._start_wait_and_stop_timer(0.06)
        self.assertEqual(self.list, [5, 6], 'lists differ')
    
    def _create_timer(self, args=(), kwargs={}):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function,
                                       args=args, kwargs=kwargs)

    def _function(self, a=None, b=None):
        self._append_to_list_if_not_none(a)
        self._append_to_list_if_not_none(b)
        self.counter += 1
    
    def _append_to_list_if_not_none(self, value):
        if value is not None:
            self.list.append(value)

    def _start_wait_and_stop_timer(self, timeout):
        self.timer.start()
        self.event.wait(timeout)
        self.timer.stop()


class TestTimerExceptions(unittest.TestCase):
    
    def setUp(self):
        self.timer = utils.timer.Timer(interval=0.05, function=self._function)
        self.timer.start()
    
    def tearDown(self):
        self.timer.stop()
    
    def test_change_interval_with_timer_running(self):
        self.assertRaises(utils.timer.TimerError, self._change_timer_interval)
    
    def test_change_args_with_timer_running(self):
        self.assertRaises(utils.timer.TimerError, self._change_timer_args)
    
    def test_change_kwargs_with_timer_running(self):
        self.assertRaises(utils.timer.TimerError, self._change_timer_kwargs)
    
    def test_change_is_running(self):
        self.assertRaises(AttributeError, self._change_timer_is_running)
    
    def test_start_timer_twice(self):
        self.assertRaises(utils.timer.TimerError, self.timer.start)
    
    def test_stop_timer_twice(self):
        self.timer.stop()
        self.assertRaises(utils.timer.TimerError, self.timer.stop)
        self.timer.start() # tearDown calls stop()
    
    def _function(self, a=None):
        pass

    def _change_timer_interval(self):
        self.timer.interval = 0.06
    
    def _change_timer_args(self):
        self.timer.args = (1.0,)
    
    def _change_timer_kwargs(self):
        self.timer.kwargs = {'a': 2.0}
    
    def _change_timer_is_running(self):
        self.timer.is_running = False


def timer_function_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTimerFunction)
    return suite


def timer_exceptions_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTimerExceptions)
    return suite


def suite():
    suite_list = []
    suite_list.append(timer_function_suite())
    suite_list.append(timer_exceptions_suite())
    return unittest.TestSuite(suite_list)
