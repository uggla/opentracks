#!/usr/bin/python
# -*- coding: utf-8 -*-

"""A module to do bla bla
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: René Ribaud <rene.ribaud@free.fr>
"""

# Import
import os
import sys
import re
from ConfigParser import RawConfigParser
import argparse
import csv
from datetime import datetime, date, time, tzinfo, timedelta
from pytz import timezone, all_timezones
import pytz
from dateutil.parser import *
from srtm import *
from math import floor

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opentracks.settings')
from django.core.management import execute_from_command_line
from ot_logbook.models import Activity, Subcategory, Category, Location, \
    Equipment, ActivityData
from django.contrib.auth.models import User

# Global variable definition
application = 'fix_elevation'
version = '1.0'
utc=pytz.utc

def main():

    argparser = argparse.ArgumentParser(description='fix elevation.')

    argparser.add_argument('user', help='user name to bind data')

    args = argparser.parse_args()
    
    # Check user
    try:
        user = User.objects.get(username=args.user)
        print 'User : ' + user.username
    except:
        sys.stderr.write('User does not exist.\n')
        sys.exit(1)

    downloader = SRTMDownloader()
    downloader.loadFileList()

    activitydata = ActivityData()
    elevation_null = ActivityData.objects.filter(elevation__isnull = True)
    for row in elevation_null[:2]:
        tile = downloader.getTile(int(floor(row.lat)),int(floor(row.lon)))
        print "%s Tile lat,lon : %i,%i srtm lat,lon : %f,%f : elevation : %f" % (row.datetime,floor(row.lat),floor(row.lon),row.lat,row.lon,tile.getAltitudeFromLatLon(row.lat,row.lon))
        row.elevation = tile.getAltitudeFromLatLon(row.lat,row.lon)
        row.save()
    print elevation_null.count()
    del activitydata

# Main
# =====

if __name__ == '__main__':
    main()
    sys.exit(0)

# The end...
