# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.query import QuerySet
from datetime import datetime, date, time, tzinfo, timedelta
from django.utils.timezone import *


from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Table Subcategory
# activity (FK)
# name
class Subcategory(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

# Table Category
# activity (FK)
# name
class Category(models.Model):
    name = models.CharField(max_length=30)
    subcategory = models.ForeignKey(Subcategory, blank = True, null = True)

    def __unicode__(self):
        return self.name

# Table Location
# activity (FK)
# location
class Location(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

# Table Equipment
# user (FK)
# activity (FK)
# name
# expectedlife
# picture
class Equipment(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    expectedlife = models.TimeField(blank = True, null = True)
    picture = models.ImageField(upload_to='photos/%Y/%m/%d',blank = True, null = True)

    def __unicode__(self):
        return self.name
# Table EquipmentData
# equipment (FK)
# datetime
# failure
# failurenotes
# maintenance
# maintenancenotes
class EquipmentData(models.Model):
    equipement = models.ForeignKey(Equipment)
    datetime = models.DateTimeField(_('event'))
    failure = models.BooleanField()
    failurenotes = models.TextField(blank = True, null = True)
    maintenance = models.BooleanField()
    maintenancenotes = models.TextField(blank = True, null = True)

    def __unicode__(self):
        return self.name

# Table Activity
# user (FK)
# category (FK)
# location
# datetime
# climbed (m)
# totaldescended (m)
# paused
# averagespeed (km/h)
# maxspeed (km/h)
# calories (kcal)
# averageheartrate (bpm)
# maxheartrate (bpm)
# averagecadence (rpm)
# maxcadence (rpm)
# averagepower (W)
# maxpower (W)
# temperature (°C)
# weather
# notes
# linkto
# public
class Activity(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category,blank = True, null = True)
    location = models.ForeignKey(Location,blank = True, null = True)
    equipment = models.ForeignKey(Equipment,blank = True, null = True)
    datetime = models.DateTimeField(_('activity start time', db_index = True))
    climbed = models.FloatField(default='0')
    descended = models.FloatField(default='0')
    paused = models.TimeField(default='00:00:00')
    averagespeed = models.FloatField()
    maxspeed = models.FloatField()
    calories = models.IntegerField(blank = True, null = True)
    averageheartrate = models.FloatField(blank = True, null = True)
    maxheartrate = models.FloatField(blank = True, null = True)
    averagecadence  = models.FloatField(blank = True, null = True)
    maxcadence = models.FloatField(blank = True, null = True)
    averagepower = models.FloatField(blank = True, null = True)
    maxpower = models.FloatField(blank = True, null = True)
    temperature = models.FloatField(blank = True, null = True)
    weather = models.CharField(max_length=100,blank = True, null = True)
    notes = models.TextField(blank = True, null = True)
    linkto = models.URLField(blank = True, null = True)
    public = models.BooleanField(default='0')
    removepeak = models.BooleanField(default='0')
    smoothing = models.IntegerField(blank = True, null = True)
    
    trackpoints = QuerySet()
    __dataloaded=False

    
    def get_all_fields(self):
        """Get all the fields from activity model.
        
        :param req_id: none
        :type req_id: na
    
        :returns: Fields
        :rtype: List
        """
        fields = []
        for f in self._meta.fields:
            fields.append(f.name)
        return(fields)
    
    def get_all_fields_values(self):
        """Get all the fields values from activity model.
        
        :param req_id: none
        :type req_id: na
    
        :returns: Fields
        :rtype: List
        """
        values = [] 
        fields = self.get_all_fields()
        for f in fields:
            values.append(getattr(self,f))
        return(values)


    def subcat(self):
        return self.category.subcategory.name
    subcat.admin_order_field = 'subcategory'
    subcat.short_description = 'subcategory'
    #def __unicode__(self):
    #    return self.datetime

    @staticmethod
    def get_id(req_id):
        """Get activity values from the DB.
        
        :param req_id: Activity id
        :type req_id: Int
    
        :returns: Activity
        :rtype: Object
        """
        return Activity.objects.get(pk = req_id)

    @staticmethod
    def get_day(day,user=""):
        """Get daily activities.
        
        :param req_id: Day
        :type req_id: Datetime
        :param req_id: Optional User
        :type req_id: String
    
        :returns: Activities
        :rtype: QuerySet
        """
	day = make_aware(day,utc)
        day = day.replace(hour=0,minute=0,second=0)
        if (user == ""):
            return Activity.objects.filter(datetime__gte = day).filter(datetime__lt = day + timedelta(days=1))
        else:
            return Activity.objects.filter(datetime__gte = day).filter(datetime__lt = day + timedelta(days=1)).filter(user__username = user)


    def __loaddata(self):
        """Load activity data.
        
        """
        self.trackpoints = ActivityData.objects.filter(activity = self.pk)
        self.__dataloaded=True

    def start(self):
        """Get acitivty start point latitude and longitude.
        
        :returns: lat and lon
        :rtype: Dictionary.
        """
        if (self.__dataloaded==False):
            self.__loaddata()
        return {'lat' : self.trackpoints[0].lat, 'lon' : self.trackpoints[0].lon}

    def speed(self):
        """Get activity speed points.
        
        :returns: Speed points
        :rtype: List
        """
        speed=list()
        if (self.__dataloaded==False):
            self.__loaddata()
        for i in range(1,self.trackpoints.count()):
            deltadist=self.trackpoints[i].distance - self.trackpoints[i-1].distance
            deltatime=self.trackpoints[i].datetime - self.trackpoints[i-1].datetime
            speed.append((deltadist / deltatime.total_seconds()) * 3600)
        return speed

    def maxspeed(self):
        """Get activity max speed
        
        :returns: Max speed
        :rtype: Float
        """
        speed = self.speed()
        return max(speed)
        
    def averagespeed(self):
        """Get activity average speed
        
        :returns: Average speed
        :rtype: Float
        """
        elementsum = 0.0
        speed = self.speed()
        nb_elements = len(speed)
        for i in speed:
            elementsum+=i    
        return elementsum/nb_elements

    def duration(self):
        """Get activity duration
        
        :returns: Duration
        :rtype: timedelta
        """
        if (self.__dataloaded==False):
            self.__loaddata()
        i = len(self.trackpoints)-1
        return self.trackpoints[i].datetime - self.trackpoints[0].datetime
        

# Table ActivityData
# activity (FK)
# lap
# distance (km)
# elevation (m)
# lat
# lon
# grade
# duration
# speed (km/h)
# heartrate (bpm)
# cadence (rpm)
# power (W)
class ActivityData(models.Model):
    activity = models.ForeignKey(Activity, db_index = True)
    datetime = models.DateTimeField(_('point timestamp'))
    lap = models.IntegerField(blank = True, null = True)
    distance = models.FloatField()
    elevation = models.FloatField(blank = True, null = True)
    lat = models.FloatField()
    lon = models.FloatField()
    #grade = models.FloatField()
    #duration = models.TimeField()
    #speed = models.FloatField()
    heartrate = models.IntegerField(blank = True, null = True)
    cadence = models.FloatField(blank = True, null = True)
    power = models.FloatField(blank = True, null = True)

    #def __unicode__(self):
    #    return self.name

# Table UserData
# user (FK)
# datetime
# weight (kg)
# bodyfat
# bmi
# skinfold
# resthr (bpm)
# athletemaxheartrate (bpm)
# systolic
# diastolic
# mood
# sleep (h)
# sleepquality
# injured
# injurednotes
# sick
# sicknotes
# missedworkout
# missedworkoutnotes
# diary
# picture
class UserData(models.Model):
    user = models.ForeignKey(User)
    datetime = models.DateTimeField(_('event'))
    weight = models.FloatField(blank = True, null = True)
    bodyfat = models.IntegerField(blank = True, null = True)
    bmi = models.IntegerField(blank = True, null = True)
    skinfold = models.IntegerField(blank = True, null = True)
    resthr = models.IntegerField(blank = True, null = True)
    athletemaxheartrate = models.IntegerField(blank = True, null = True)
    systolic = models.IntegerField(blank = True, null = True)
    diastolic = models.IntegerField(blank = True, null = True)
    mood = models.CharField(max_length=100,blank = True, null = True)
    sleep = models.TimeField(blank = True, null = True)
    sleepquality = models.CharField(max_length=10,blank = True, null = True)
    injured = models.BooleanField()
    injurednotes = models.TextField(blank = True, null = True)
    sick = models.BooleanField()
    sicknotes = models.TextField(blank = True, null = True)
    missed = models.BooleanField()
    missedworkoutnotes = models.TextField(blank = True, null = True)
    diary = models.TextField(blank = True, null = True)
    picture = models.ImageField(upload_to='photos/%Y/%m/%d',blank = True, null = True)

    def __unicode__(self):
        return self.user.username

# Tables Settings
class GlobalSettings(models.Model):
    key = models.CharField(max_length=1024)
    value = models.CharField(max_length=1024)

class UserSettings(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=1024)
    value = models.CharField(max_length=1024)

# Currently unknown fields
# intensity ?
# zonetype ?
# zonecategory ?
# zonename ?
# percent ?
# laptype ?
# caloriesconsumed (kcal) ?
