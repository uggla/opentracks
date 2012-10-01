# -*- coding: utf-8 -*-
from django.db import models

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
    
    def subcat(self):
        return self.category.subcategory.name
    subcat.admin_order_field = 'subcategory'
    subcat.short_description = 'subcategory'
    #def __unicode__(self):
    #    return self.datetime


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
    elevation = models.FloatField()
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
# units
class Settings(models.Model):
    units = models.BooleanField()

    #def __unicode__(self):
    #    return self.name
    
# 

# Currently unknown fields
# intensity ?
# zonetype ?
# zonecategory ?
# zonename ?
# percent ?
# laptype ?
# caloriesconsumed (kcal) ?
