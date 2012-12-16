#!/usr/bin/python
# -*- coding: utf-8 -*-
"""A module to do bla bla
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: René Ribaud <rene.ribaud@free.fr>
"""

import numpy as np
from math import ceil
import unittest
import pprint

smoothing = 0


class Smoothing:

    """Smoothing of elements
    :param request: HTTP request parameter
    :type request: HttpRequest
    :param date : date parameter in Y-m-d format
    :type request: String
    :param request : Activity id or "latest"
    :type request: String

    :returns: HttpResponse
    :rtype: HttpPage
    """

    def __init__(self, x, y, smoothing_factor,):
        global smoothing
        smoothing = smoothing_factor
        self.x = x
        self.y = y
        self.smoothing_segment_list = []

        if len(x) != len(y):
            raise 'Provided lists have not the same size.'

        self.calculate()

    def calculate(self):
        nbseg = ceil(self.x[len(self.x) - 1] / float(smoothing))
        for seg in range(int(nbseg)):
            self.smoothing_segment_list.append(SmoothingSegment())

        # Push point in the correct segment

        for i in range(len(self.x)):
            for seg in self.smoothing_segment_list:
                if seg.startx() < self.x[i] and self.x[i] <= seg.endx():
                    seg.originalx.append(self.x[i])
                    seg.originaly.append(self.y[i])

    def __del__(self):
        for smoothing_segment in self.smoothing_segment_list:
            self.smoothing_segment_list.remove(smoothing_segment)
            del smoothing_segment


class SmoothingSegment:

    count = 0

    def __init__(self):
        self.id = SmoothingSegment.count
        SmoothingSegment.count += 1
        self.originalx = []
        self.originaly = []
        self.correctedx = []
        self.correctedy = []

    def get_id(self):
        return self.id

    def get_originalx(self):
        return self.originalx

    def get_originaly(self):
        return self.originaly

    def startx(self):
        return self.get_id() * smoothing

    def endx(self):
        return (self.get_id() + 1) * smoothing

    def average(self):
        return float(np.mean(self.originaly))

    def __del__(self):
        SmoothingSegment.count -= 1


class point:

    pass


class SmoothingTest(unittest.TestCase):

    def setUp(self):
        self.smooth = Smoothing([1, 2, 3, 4, 5], [10, 20, 30, 40, 40],
                                2)

    def test_originalx(self):
        self.assertEqual(self.smooth.smoothing_segment_list[0].get_originalx(),
                         [1, 2])
        self.assertEqual(self.smooth.smoothing_segment_list[1].get_originalx(),
                         [3, 4])
        self.assertEqual(self.smooth.smoothing_segment_list[2].get_originalx(),
                         [5])
        del self.smooth

    def test_originaly(self):
        self.assertEqual(self.smooth.smoothing_segment_list[0].get_originaly(),
                         [10, 20])
        self.assertEqual(self.smooth.smoothing_segment_list[1].get_originaly(),
                         [30, 40])
        self.assertEqual(self.smooth.smoothing_segment_list[2].get_originaly(),
                         [40])
        del self.smooth

    def test_average(self):
        self.assertEqual(self.smooth.smoothing_segment_list[0].get_originalx(),
                         [1, 2])
        self.assertEqual(self.smooth.smoothing_segment_list[0].average(),
                         float(15))
        self.assertEqual(self.smooth.smoothing_segment_list[1].average(),
                         float(35))
        self.assertEqual(self.smooth.smoothing_segment_list[2].average(),
                         float(40))
        self.assertEqual(self.smooth.smoothing_segment_list[0].get_originalx(),
                         [1, 2])
        del self.smooth


# DEBUG ONLY

if __name__ == '__main__':
    print 'Running tests :'
    unittest.main()
