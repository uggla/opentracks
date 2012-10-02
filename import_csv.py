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
            return False
        if (value == ''):
            return False

        return True
            
    def import_activitydata():
        activitydata = ActivityData()
        activitydata.datetime=activity.datetime
        activitydata.activity = activity
        if ( checkfield(row[config.getfield('lap')]) ) :
            activitydata.lap = row[config.getfield('lap')]
        activitydata.distance = row[config.getfield('distance')]
        if ( checkfield(row[config.getfield('elevation')]) ) :
            activitydata.elevation = row[config.getfield('elevation')]
        activitydata.lat = row[config.getfield('lat')]
        activitydata.lon = row[config.getfield('lon')]
        #activitydata.grade = row[config.getfield('grade')]
        #activitydata.duration = row[config.getfield('duration')]
        #activitydata.speed = row[config.getfield('speed')]
        if ( checkfield(row[config.getfield('heartrate')]) ) :
            activitydata.heartrate = round_int(float(row[config.getfield('heartrate')]))
        if ( checkfield(row[config.getfield('cadence')]) ) :
            activitydata.cadence = row[config.getfield('cadence')]
        if ( checkfield(row[config.getfield('power')]) ) :
            activitydata.power = row[config.getfield('power')]

        if not ( activitydata.distance == ''  or
                 activitydata.lat == '' or
                 activitydata.lon == ''):
            activitydata.save()
        del activitydata

    def convert_utc(value):
        timestamp = parse(value)
        timestamp = mytz.localize(timestamp)
        timestamp = timestamp.astimezone(utc)
        return timestamp

    def convert_duration(value):
        timestamp = parse(value)
        timestamp = timestamp.time()
        return timestamp

    def round_int(value):
        return int(round(value))
        
    def show_timezones():
        for zone in all_timezones:
            print zone
        sys.exit(0)


    print application + ' ' + version
    print


    # Subcategory.objects.all()
    # p = Subcategory(name = "Essai")
    # p.save()

    argparser = argparse.ArgumentParser(description='Import csv data.')

    argparser.add_argument('user', help='user name to bind data')
    argparser.add_argument('timezone', help='timezone used to import data')
    argparser.add_argument('filename', help='csv filename to import')
    argparser.add_argument('--timezone', help='show available timezone',
                           action='store_true', dest='tzavail')
    argparser.add_argument('--force_new', help='Force to add an activity even if already in the DB. This is used mainly for debugging purpose',
                           action='store_true', dest='fnew')


    args = argparser.parse_args()
    
    config = ImportConfFile()
    config.read(cfgfile)

    # Show timezone if required
    if ( args.tzavail == True ):
        show_timezones()

    # Check user
    try:
        user = User.objects.get(username=args.user)
        print 'User : ' + user.username
    except:
        sys.stderr.write('User does not exist.\n')
        sys.exit(1)

    try:
        mytz = timezone(args.timezone)
        print 'Timezone for data : ' + mytz.zone
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
                print 'Category imported.'
                print 'No subcategory found'
        else:

            try:
                subcategory = \
                    Subcategory.objects.get(name=row[config.getfield('subcategory')])
            except:
                subcategory.name = row[config.getfield('subcategory')]
                subcategory.save()
                print 'Subcategory imported.'

            try:
                category = \
                    Category.objects.get(name=row[config.getfield('category')])
            except:
                category.name = row[config.getfield('category')]
                category.subcategory = subcategory
                category.save()
                print 'Category imported.'

        # Import location

        try:
            location = \
                Location.objects.get(name=row[config.getfield('location')])
        except:
            location.name = row[config.getfield('location')]
            location.save()
            print 'Location imported.'

        # Import equipment

        try:
            equipment = \
                Equipment.objects.get(name=row[config.getfield('equipment')])
        except:
            equipment.name = row[config.getfield('equipment')]
            equipment.user = user
            equipment.save()
            print 'Equipement imported.'

        # Import activity

        activity.user = user
        activity.category = category
        activity.location = location
        activity.equipment = equipment

        activity.datetime = convert_utc(row[config.getfield('datetime')])
        # Check if an activity with same timestamp already exist
        if not ( args.fnew == True ):
            existing_activity = Activity.objects.filter(datetime = activity.datetime)
            if not ( len(existing_activity) == 0):
                sys.stderr.write('One or several existing activity is available with timestamp : ')
                sys.stderr.write(activity.datetime.isoformat())
                sys.stderr.write('\n')
                sys.exit(1)
 
        activity.climbed = row[config.getfield('climbed')]
        activity.descended = row[config.getfield('descend')]
        activity.paused = convert_duration (row[config.getfield('paused')])

        activity.averagespeed = row[config.getfield('averagespeed')]
        activity.maxspeed = row[config.getfield('maxspeed')]
        activity.calories = round_int(float(row[config.getfield('calories')]))

        if ( checkfield(row[config.getfield('averageheartrate')]) ) :
            activity.averageheartrate = row[config.getfield('averageheartrate')]
        if ( checkfield(row[config.getfield('maxheartrate')]) ) :
            activity.maxheartrate = row[config.getfield('maxheartrate')]
        if ( checkfield(row[config.getfield('averagecadence')]) ) :
            activity.averagecadence = row[config.getfield('averagecadence')]
        if ( checkfield(row[config.getfield('maxcadence')]) ) :
            activity.maxcadence = row[config.getfield('maxcadence')]
        if ( checkfield(row[config.getfield('averagepower')]) ) :
            activity.averagepower = row[config.getfield('averagepower')]
        if ( checkfield(row[config.getfield('maxpower')]) ) :
            activity.maxpower = row[config.getfield('maxpower')]
        if ( checkfield(row[config.getfield('temperature')]) ) :
            activity.temperature = row[config.getfield('temperature')]
        if ( checkfield(row[config.getfield('weather')]) ) :
            activity.weather = row[config.getfield('weather')]
        if ( checkfield(row[config.getfield('notes')]) ) :
            activity.notes = row[config.getfield('notes')]

        activity.save()
        print 'Activity imported.'


        # Import activitydata from first line
        import_activitydata()
        
    #for row in data[2:5]:
    for row in data[2:]:
        previous_timestamp=activity.datetime
        activity.datetime = convert_utc(row[config.getfield('datetime')])
        if (activity.datetime < previous_timestamp):
            break
        import_activitydata()
        
    print 'ActivityData imported.'

# Main
# =====

if __name__ == '__main__':
    main()
    sys.exit(0)

# The end...
