"""
Timer
"""

import time


class Timer:

    def __init__(self):
        self.s = 0
        self.e = 0
        self.elapsed_str = 0
        self.elapsed = 0

    def start(self):
        self.s = time.time()

    def end(self):
        self.e = time.time()
        self.elapsed_str = str(self.e - self.s)
        self.elapsed = self.e - self.s

    def reset(self):
        self.s = 0
        self.e = 0
        self.elapsed = 0
        self.elapsed_str = 0


