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
from pytz import timezone
import pytz
from dateutil.parser import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'opentracks.settings')
from django.core.management import execute_from_command_line
from logbook.models import Activity, Subcategory, Category, Location, \
    Equipment, ActivityData
from django.contrib.auth.models import User

# Global variable definition
application = 'import_csv'
version = '1.0'
cfgfile = 'import_csv.cfg'
utc=pytz.utc

# Class definition
class ImportConfFile(RawConfigParser):

    def __init__(self):
        RawConfigParser.__init__(self) 

    def getfield(self, field):
        return (int(self.get('Fields' , field)) - 1)


def main():
    data = list()
    activity = Activity()
    category = Category()
    subcategory = Subcategory()
    location = Location()
    equipment = Equipment()
    
    def checkfield(value):
        test = re.search('ignore', value, re.I)
        if test is not None:
            return 0
        if (value == ''):
            return 0

        return 1
            
    def import_activitydata():
        activitydata = ActivityData()
        activitydata.datetime=activity.datetime
        activitydata.activity = activity
        if ( checkfield(row[config.getfield('lap')]) ) :
            activitydata.lap = row[config.getfield('lap')]
        activitydata.distance = row[config.getfield('distance')]
        activitydata.elevation = row[config.getfield('elevation')]
        activitydata.lat = row[config.getfield('lat')]
        activitydata.lon = row[config.getfield('lon')]
        #activitydata.grade = row[config.getfield('grade')]
        #activitydata.duration = row[config.getfield('duration')]
        #activitydata.speed = row[config.getfield('speed')]
        if ( checkfield(row[config.getfield('heartrate')]) ) :
            activitydata.heartrate = row[config.getfield('heartrate')]
        if ( checkfield(row[config.getfield('cadence')]) ) :
            activitydata.cadence = row[config.getfield('cadence')]
        if ( checkfield(row[config.getfield('power')]) ) :
            activitydata.power = row[config.getfield('power')]
        if not ( activitydata.distance == ''  and
             activitydata.elevation == '' and
             activitydata.lat == '' and
             activitydata.lon == ''):
            activitydata.save()
        del activitydata

    def convert_utc(value):
        timestamp = parse(value)
        timestamp = mytz.localize(timestamp)
        timestamp = timestamp.astimezone(utc)
        return timestamp
        

    print application + ' ' + version
    print


    # Subcategory.objects.all()
    # p = Subcategory(name = "Essai")
    # p.save()

    argparser = argparse.ArgumentParser(description='Import csv data.')

    argparser.add_argument('user', help='user name')
    argparser.add_argument('timezone', help='timezone')
    argparser.add_argument('filename', help='csv filename to import')

    # argparser.add_argument('-v', '--verbose', dest='verbose',
    #                    action='store_true',
    #                    help='verbose output, print output fron par2 and unrar'
    #                    )

    # argparser.add_argument('-t', '--test', dest='test', action='store_true'
    #                    , help='do not extract file only verify them')

    # argparser.add_argument('-c', '--curse', dest='curse',
    #                    action='store_true',
    #                    help='use curses Text User Interface')

    args = argparser.parse_args()

    config = ImportConfFile()
    config.read(cfgfile)

    try:
        user = User.objects.get(username=args.user)
    except:
        sys.stderr.write('User does not exist.\n')
        sys.exit(1)

    try:
        mytz = timezone(args.timezone)
        print mytz.zone
    except:
        sys.stderr.write('Unknown timezone.\n')
        sys.exit(1)
    

    with open(args.filename, 'rb') as f:

        # reader = csv.reader(f, delimiter= config.get('File','delimiter'), dialect=csv.excel)

        reader = csv.reader(f ,
                            delimiter=config.get('File', 'delimiter'))
        for row in reader:
            data.append(row) # Slurp data into memory

    for row in data[1:2]:

        # Import category and subcategory

        if row[config.getfield('category')].decode('utf-8') \
            == 'Mes activités'.decode('utf-8'):
            try:
                category = \
                    Category.objects.get(name=row[config.getfield('subcategory')])
            except:
                category.name = row[config.getfield('subcategory')]
                category.save()
        else:

            try:
                subcategory = \
                    Subcategory.objects.get(name=row[config.getfield('subcategory')])
            except:
                subcategory.name = row[config.getfield('subcategory')]
                subcategory.save()

            try:
                category = \
                    Category.objects.get(name=row[config.getfield('category')])
            except:
                category.name = row[config.getfield('category')]
                category.subcategory = subcategory
                category.save()

        # Import location

        try:
            location = \
                Location.objects.get(name=row[config.getfield('location')])
        except:
            location.name = row[config.getfield('location')]
            location.save()

        # Import equipment

        try:
            equipment = \
                Equipment.objects.get(name=row[config.getfield('equipment')])
        except:
            equipment.name = row[config.getfield('equipment')]
            equipment.user = user
            equipment.save()

        # Import activity

        activity.user = user
        activity.category = category
        activity.location = location
        activity.equipment = equipment

        activity.datetime = convert_utc(row[config.getfield('datetime')])

        activity.climbed = row[config.getfield('climbed')]
        activity.descended = row[config.getfield('descend')]
        activity.paused = time(12, 30)

        activity.averagespeed = row[config.getfield('averagespeed')]
        activity.maxspeed = row[config.getfield('maxspeed')]
        activity.calories = row[config.getfield('calories')]

        activity.averageheartrate = row[config.getfield('averageheartrate')]
        activity.maxheartrate = row[config.getfield('maxheartrate')]

        # Still missing fields

        activity.public = False
        activity.save()


        # Import activitydata from first line
        import_activitydata()
        
    #for row in data[2:5]:
    for row in data[2:]:
        previous_timestamp=activity.datetime
        activity.datetime = convert_utc(row[config.getfield('datetime')])
        if (activity.datetime < previous_timestamp):
            break
        import_activitydata()
        

# Main
# =====

if __name__ == '__main__':
    main()
    sys.exit(0)

# The end...
