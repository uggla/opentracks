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

# Defined smoothing factor for the entire module.
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

    def __init__(self,smoothing_factor, x = [], y = [], debug = False):
        global smoothing
        smoothing = smoothing_factor
        self.x = x
        self.y = y
        self.__debug = debug

        @property
        def debug(self):
            return self.__debug
        @debug.setter
        def debug(self, value):
            self.__debug = value

        @property
        def ycorrected(self):
            return self.__ycorrected
        self.ycorrected = []

        self.smoothing_segment_list = []


        if (len(self.x) > 0):
            self.calculate()

    def calculate(self):
        print self.smoothing_segment_list
        if len(self.x) != len(self.y):
            raise Exception('Provided lists have not the same size.')

        nbseg = ceil(self.x[len(self.x) - 1] / float(smoothing))
        for seg in range(int(nbseg)):
            self.smoothing_segment_list.append(SmoothingSegment())

        # Push point in the correct segment

        for i in range(len(self.x)):
            for seg in self.smoothing_segment_list:
                if seg.startx() < self.x[i] and self.x[i] <= seg.endx():
                    seg.originalx.append(self.x[i])
                    seg.originaly.append(self.y[i])


        # Calculate y offset of each segments
        last_known_value=0
        for seg in range(0,len(self.smoothing_segment_list)):
            print "nb of data %f" % len(self.smoothing_segment_list[seg].originalx)
            if (len(self.smoothing_segment_list[seg].originalx) == 0 and seg == 0): # smoothing value is too small, so there are no points in this segment.
                   raise "Smoothing value is too small."

            if (len(self.smoothing_segment_list[seg].originalx) > 0 and seg == 0): # we have values in the segment but this is the first one.
                   #self.smoothing_segment_list[seg].yoffset  = self.smoothing_segment_list[seg].originaly[0]
                   self.smoothing_segment_list[seg].yoffset  = (self.smoothing_segment_list[seg].average() - self.smoothing_segment_list[seg].originaly[0])/(self.smoothing_segment_list[seg].endx()-self.smoothing_segment_list[seg].originalx[0])
                   #self.smoothing_segment_list[seg].yoffset  = 0

            if (seg > 0): # For all non empty segments except the first one.
                   if (len(self.smoothing_segment_list[seg-1].originalx) > 0): # Do not calculate average if previous segment was empty, this will cause an error.
                       self.smoothing_segment_list[seg].yoffset  = self.smoothing_segment_list[seg-1].average()
                       print "Average : %f" % self.smoothing_segment_list[seg-1].average()
                       last_known_value = self.smoothing_segment_list[seg-1].average()
                   else:
                       self.smoothing_segment_list[seg].yoffset  = last_known_value

        # Calculate gradient for each segment
        result = []
        for seg in self.smoothing_segment_list:
            if (len(seg.originalx) > 0):
                seg.gradient = (seg.average() - seg.yoffset) / (seg.endx() - seg.startx())
            else:
                seg.gradient = 0


        # Linear correction of the points
        result = []
        for seg in self.smoothing_segment_list:
            if (len(seg.originalx) > 0):
                segresult=np.array(seg.originalx)
                segresult=segresult[:] - seg.startx()
                segresult=segresult[:] * seg.gradient + seg.yoffset
                result+=list(segresult)
        self.ycorrected=result

        if (self.__debug != True):
            self.__cleanup_segment_list()
            
                
    def __cleanup_segment_list(self):
        del(self.smoothing_segment_list[:])

    def __del__(self):
        self.__cleanup_segment_list()

class SmoothingSegment:

    count = 0

    def __init__(self):
        self.id = SmoothingSegment.count
        SmoothingSegment.count += 1
        self.originalx = []
        self.originaly = []
	self.yoffset=0
        self.gradient=0	

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

    def test_simple_internal_smoothing(self):
        self.smooth = Smoothing(2, [1, 2, 3, 4, 5], [10, 20, 30, 40, 40],True)
        self.assertEqual(self.smooth.smoothing_segment_list[0].get_originalx(), [1, 2])
        self.assertEqual(self.smooth.smoothing_segment_list[1].get_originalx(), [3, 4])
        self.assertEqual(self.smooth.smoothing_segment_list[2].get_originalx(), [5])
        self.assertEqual(self.smooth.smoothing_segment_list[0].get_originaly(), [10, 20])
        self.assertEqual(self.smooth.smoothing_segment_list[1].get_originaly(), [30, 40])
        self.assertEqual(self.smooth.smoothing_segment_list[2].get_originaly(), [40])
        self.assertEqual(self.smooth.smoothing_segment_list[0].startx(), 0)
        self.assertEqual(self.smooth.smoothing_segment_list[1].startx(), 2)
        self.assertEqual(self.smooth.smoothing_segment_list[2].startx(), 4)
        self.assertEqual(self.smooth.smoothing_segment_list[0].endx(), 2)
        self.assertEqual(self.smooth.smoothing_segment_list[1].endx(), 4)
        self.assertEqual(self.smooth.smoothing_segment_list[2].endx(), 6)
        self.assertEqual(self.smooth.smoothing_segment_list[0].average(), 15)
        self.assertEqual(self.smooth.smoothing_segment_list[1].average(), 35)
        self.assertEqual(self.smooth.smoothing_segment_list[2].average(), 40)
        self.assertEqual(self.smooth.smoothing_segment_list[0].yoffset, 5)
        self.assertEqual(self.smooth.smoothing_segment_list[1].yoffset, 15)
        self.assertEqual(self.smooth.smoothing_segment_list[2].yoffset, 35)
        self.assertEqual(self.smooth.smoothing_segment_list[0].gradient, 5)
        self.assertEqual(self.smooth.smoothing_segment_list[1].gradient, 10)
        self.assertEqual(self.smooth.smoothing_segment_list[2].gradient, 2.5)
        self.assertEqual(self.smooth.ycorrected, [10.0, 15.0, 25.0, 35.0, 37.5])
        del self.smooth

    def test_simple_smoothing(self):
        self.smooth = Smoothing(2, [1, 2, 3, 4, 5], [10, 20, 30, 40, 40])
        self.assertEqual(self.smooth.ycorrected, [10.0, 15.0, 25.0, 35.0, 37.5])
        del self.smooth

    def test_simple_smoothing_twice_1(self):
        self.smooth = Smoothing(2, [1, 2, 3, 4, 5], [10, 20, 30, 40, 40])
        self.assertEqual(self.smooth.ycorrected, [10.0, 15.0, 25.0, 35.0, 37.5])
        self.smooth.calculate()
        self.assertEqual(self.smooth.ycorrected, [10.0, 15.0, 25.0, 35.0, 37.5])
        del self.smooth

    def test_simple_smoothing_twice_2(self):
        self.smooth = Smoothing(2, [1, 2, 3, 4, 5], [10, 20, 30, 40, 40])
        self.assertEqual(self.smooth.ycorrected, [10.0, 15.0, 25.0, 35.0, 37.5])
        self.smooth = Smoothing(2, [1, 2, 3, 4, 5], [10, 20, 30, 40, 40])
        self.assertEqual(self.smooth.ycorrected, [10.0, 15.0, 25.0, 35.0, 37.5])
        del self.smooth
 
    def test_smoothing_list_size_error(self):
        with self.assertRaises(Exception) as context:
            Smoothing(2, [1, 2, 3, 4, 5,6], [10, 20, 30, 40, 40])
        self.assertEqual(context.exception.message, 'Provided lists have not the same size.')

# DEBUG ONLY

if __name__ == '__main__':
    print 'Running tests :'
    unittest.main()
