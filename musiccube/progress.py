#
# progress.py
#
# Copyright (C) 2015 Jeremiah J. Leonard
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from os import linesep
from sys import stdout

class Progress:

    STEPS = 50
    TITLE = 25

    def __init__(self, title, total):

        self.title = title
        self.total = total
        self.count = 0
        self.last = 0
        self.width = float(total) / float(self.STEPS)
        stdout.write(self.title.ljust(self.TITLE))

    def display(self):

        self.count += 1
        curr = int(self.count / self.width)
        dots = curr - self.last
        for i in range(dots):
            stdout.write(".")
        if self.count == self.total:
            stdout.write(linesep)
        stdout.flush()
        self.last = curr
