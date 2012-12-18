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
   
        last_known_value=0
        for seg in range(0,len(self.smoothing_segment_list)):
            print "nb of data %f" % len(self.smoothing_segment_list[seg].originalx)
            if (len(self.smoothing_segment_list[seg].originalx) > 0): # Check if we have values on this segment
                if (seg == 0):
                   self.smoothing_segment_list[seg].yoffset  = self.smoothing_segment_list[seg].originaly[0]
                else:
                   if (len(self.smoothing_segment_list[seg-1].originalx) > 0): # Do not calculate average if previous segment was empty
                       self.smoothing_segment_list[seg].yoffset  = self.smoothing_segment_list[seg-1].average()
                       print "Average : %f" % self.smoothing_segment_list[seg-1].average()
                       last_known_value = self.smoothing_segment_list[seg-1].average()
                   else:
                       self.smoothing_segment_list[seg].yoffset  = last_known_value
                                      
            else:
                if (seg == 0):
                   raise "Smoothing value is too small."
                else:
                   if (len(self.smoothing_segment_list[seg-1].originalx) > 0): # Do not calculate average if previous segment was empty
                       self.smoothing_segment_list[seg].yoffset  = self.smoothing_segment_list[seg-1].average()
                       print "Average : %f" % self.smoothing_segment_list[seg-1].average()
                       last_known_value = self.smoothing_segment_list[seg-1].average()
                   else:
                       self.smoothing_segment_list[seg].yoffset  = last_known_value
                
                

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
	self.yoffset=0

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
        self.smooth = Smoothing([1, 2, 3, 4, 9], [10, 20, 30, 40, 40],
                                2)

#    def test_originalx(self):
#        self.assertEqual(self.smooth.smoothing_segment_list[0].get_originalx(),
#                         [1, 2])
#        self.assertEqual(self.smooth.smoothing_segment_list[1].get_originalx(),
#                         [3, 4])
#        self.assertEqual(self.smooth.smoothing_segment_list[2].get_originalx(),
#                         [5])
#        del self.smooth
#
#    def test_originaly(self):
#        self.assertEqual(self.smooth.smoothing_segment_list[0].get_originaly(),
#                         [10, 20])
#        self.assertEqual(self.smooth.smoothing_segment_list[1].get_originaly(),
#                         [30, 40])
#        self.assertEqual(self.smooth.smoothing_segment_list[2].get_originaly(),
#                         [40])
#        del self.smooth
#
#    def test_average(self):
#        self.assertEqual(self.smooth.smoothing_segment_list[0].average(),
#                         float(15))
#        self.assertEqual(self.smooth.smoothing_segment_list[1].average(),
#                         float(35))
#        self.assertEqual(self.smooth.smoothing_segment_list[2].average(),
#                         float(40))
#        del self.smooth

    def test_offset(self):
        print self.smooth.smoothing_segment_list[0].get_originalx()
        print self.smooth.smoothing_segment_list[1].get_originalx()
        print self.smooth.smoothing_segment_list[2].get_originalx()
        print self.smooth.smoothing_segment_list[3].get_originalx()
        print self.smooth.smoothing_segment_list[4].get_originalx()
        print self.smooth.smoothing_segment_list[0].yoffset
        print self.smooth.smoothing_segment_list[1].yoffset
        print self.smooth.smoothing_segment_list[2].yoffset
        print self.smooth.smoothing_segment_list[3].yoffset
        print self.smooth.smoothing_segment_list[4].yoffset


# DEBUG ONLY

if __name__ == '__main__':
    print 'Running tests :'
    unittest.main()
