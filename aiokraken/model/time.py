import time

# https://wiki.python.org/moin/WorkingWithTime
class Time:
    """
    A cross exchange python representation of time.
    Includes domain specific semantic about correctness of data.

    TODO : Uses rfc 3339 rfc 1123  iso8601 ???
    """

    def __init__(self, unixtime):
        self._unixtime = unixtime

    @property
    def unixtime(self):
        return self._unixtime

    def __repr__(self):
        return time.ctime(self._unixtime)

    def __str__(self):
        return time.ctime(self._unixtime)
