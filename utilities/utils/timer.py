"""Repeating timer"""

import threading
import time


class Timer(object):
    """Repeating timer that calls function with the provided arguments every
    time interval is elapsed.
    """
    def __init__(self, interval, function, args=[], kwargs={}):
        """interval -- interval between function calls, in seconds
        function -- function to be called
        args -- tuple of arguments to be passed to function
        kwargs -- dictionary of arguments to be passed to function
        """
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self._interval = interval
        self._is_running = False

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, value):
        """Change interval, restarting timer if already running.
        
        value -- new interval in seconds
        """
        if self._is_running:
            self.stop()
            was_running = True
        else:
            was_running = False
        self._interval = value
        if was_running:
            self.start()
    
    def start(self):
        """Start timer; first function call occurs after interval is elapsed.
        """
        if self._is_running:
            return
        self._is_first_run = True
        self._is_running = True
        self._next_call = time.time()
        self._timer()

    def stop(self):
        if not self._is_running:
            return
        self._is_running = False
        self._t.cancel()

    def _timer(self):
        if self._is_first_run:
            self._is_first_run = False
        else:
            self.function(*self.args, **self.kwargs)

        self._next_call += self.interval
        self._t = threading.Timer(self._next_call-time.time(), self._timer)
        self._t.start()
