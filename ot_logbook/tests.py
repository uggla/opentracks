"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from ot_logbook.models import Activity
from datetime import datetime, date, time, tzinfo, timedelta

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_basic_multiplication(self):
        """
        Tests that 2 * 2 always equals 4.
        """
        self.assertEqual(2 * 2, 4)

class ActivityTest(TestCase):
    def test_create_activity(self):
        """
        Get activity id=418
        Make sure start point is {'lat': 45.2759208679199, 'lon': 5.6514458656311}
        """
        act=Activity.get_id(418)
        self.assertEqual(act.start(),{'lat': 45.2759208679199, 'lon': 5.6514458656311})
