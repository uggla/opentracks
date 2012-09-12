#!/usr/bin/python
# -*- coding: utf-8 -*-

"""A module to do bla bla
   :platform: Unix
   :synopsis: A useful module indeed.

.. moduleauthor:: René Ribaud <rene.ribaud@free.fr>
"""


import os
import sys
import ConfigParser
import argparse
import csv
from datetime import datetime, date, time, tzinfo, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opentracks.settings")
from django.core.management import execute_from_command_line
from logbook.models import Activity, Subcategory, Category, Location, Equipment
from django.contrib.auth.models import User

application = 'import_csv'
version = '1.0'
cfgfile = 'import_csv.cfg'

# A UTC class.
class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)




def main():
    data = list()

    print application + ' ' + version

#Subcategory.objects.all()
#p = Subcategory(name = "Essai")
#p.save()

    parser = \
        argparse.ArgumentParser(description='Import csv data.'
                                )

    parser.add_argument('filename', help='csv filename to import')
    parser.add_argument('user', help='user name')
    #parser.add_argument('-v', '--verbose', dest='verbose',
    #                    action='store_true',
    #                    help='verbose output, print output fron par2 and unrar'
    #                    )

    #parser.add_argument('-t', '--test', dest='test', action='store_true'
    #                    , help='do not extract file only verify them')

    #parser.add_argument('-c', '--curse', dest='curse',
    #                    action='store_true',
    #                    help='use curses Text User Interface')

    args = parser.parse_args()



    config = ConfigParser.RawConfigParser()
    config.read(cfgfile)

    with open(args.filename, 'rb') as f:
        #reader = csv.reader(f, delimiter= config.get('File','delimiter'), dialect=csv.excel)
        reader = csv.reader(f, delimiter= config.get('File','delimiter'))
        for row in reader:
            data.append(row)

        for row in data[1:2]:
	    user = User.objects.get(username=args.user)
	    activity = Activity()
	    category = Category()
            subcategory = Subcategory()
            location = Location()
            equipment = Equipment()
	    

            # Import category and subcategory
            if row[int(config.get('Fields','category')) - 1].decode('utf-8') == 'Mes activités'.decode('utf-8'):
	        try:
                    category = Category.objects.get(name = row[int(config.get('Fields','subcategory')) - 1])
		except:
                    category.name = row[int(config.get('Fields','subcategory')) - 1]
                    category.save()

            else:
	        try:
                    subcategory = Subcategory.objects.get(name = row[int(config.get('Fields','subcategory')) - 1])
	        except:
                    subcategory.name = row[int(config.get('Fields','subcategory')) - 1]
                    subcategory.save()

		try:
                    category = Category.objects.get(name = row[int(config.get('Fields','category')) - 1])
                except:
	            category.name = row[int(config.get('Fields','category')) - 1]
	            category.subcategory= subcategory
                    category.save()

            # Import location
	    try:
                location = Location.objects.get(name = row[int(config.get('Fields','location')) - 1])
            except: 
                location.name = row[int(config.get('Fields','location')) - 1]
                location.save()

            # Import equipment
	    try:
                equipment = Equipment.objects.get(name = row[int(config.get('Fields','equipment')) - 1])
            except: 
                equipment.name = row[int(config.get('Fields','equipment')) - 1]
                equipment.user = user
                equipment.save()



            # Import activity
	    activity.user = user
            activity.category = category
            activity.location = location
            activity.equipment = equipment
            activity.datetime = datetime.strptime(row[int(config.get('Fields','datetime')) - 1], "%Y-%m-%d %H:%M:%S")
            activity.datetime = activity.datetime.replace(tzinfo=UTC())
            activity.climbed = 0
            activity.descended = 0
            activity.paused = time(12,30)
            activity.averagespeed = 0
            activity.maxspeed = 0
            activity.public = True
            activity.save()
            #sys.exit(0)


# Main
# =====

if __name__ == '__main__':
    main()
    sys.exit(0)

# The end...
