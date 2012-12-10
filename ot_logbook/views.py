# Create your views here.

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Activity, GlobalSettings, UserSettings
from datetime import datetime, date, time, tzinfo, timedelta
import json
from django.http import HttpResponse
from urllib import unquote, quote
from django.http import Http404
from dateutil.parser import *
from django.utils.timezone import *

def last_week_activity(request):
    """Get activities from last 7 days
    
    :param request: HTTP request parameter
    :type request: HttpRequest

    :returns: HttpResponse
    :rtype: HttpPage
    """
    lastweek = Activity.objects.filter(public = True).filter(datetime__gt = make_aware(datetime.now(),utc)-timedelta(days=7))
    return render(request, 'ot_logbook/lastweek_activity.html', {'lastweek': lastweek})

def public_activities(request):
    """Get public activities.
    
    :param request: HTTP request
    :type request: HttpRequest

    :returns: HttpResponse
    :rtype: HttpPage
    """
    if request.method == 'POST':
        msg = __visible_field_save_or_reset(request.POST,request.user)
        return HttpResponse(msg)

    else:
        fields_data = __provide_fields_data(Activity(),"datatable_activity_fields")
        activities = Activity.objects.filter(public = True)

        return render(request, 'ot_logbook/public_activities.html', {'fields': fields_data["fields"], 'activities': activities, 'visible_fields': fields_data["visible_fields"] })

def __provide_fields_data(model_instance,key):
    """ Provide fields name and visible fields.
    
    :param request: Model instance to do introspection and get fields name.
    :type request: Model instance
    :param request: Key used to store visible fields in global or user settings.
    :type request: String

    :returns: Dictionary containing fields names and visible_fields
    :rtype: Dictionary key1 : fields, key2 : visible_fields
    """
    global UserSettings
    global GlobalSettings
    data = {}
    data["fields"] = model_instance.get_all_fields()
    # Get user or global settings regarding fields visible
    try:
        visible_fields = UserSettings.objects.get(key = key)
    except:
        visible_fields = GlobalSettings.objects.get(key = key)

    vf = visible_fields.value
    data["visible_fields"] = json.loads(vf)
    return(data)


def __visible_field_save_or_reset(req,user):
    """ Manage ajax post to save or reset column selector
    
    :param request: Request
    :type request: request.POST
    :param request: User
    :type request: request.user

    :returns: Message
    :rtype: String
    """
    if (req.get('action') != 'save' and req.get('action') != 'reset'):
        raise Http404

    if (req.get('action') == 'save'):
        visible_fields = req.get('visible_fields')
        visible_fields = visible_fields.split(',')
        #print visible_fields
        try:
            usersettings = UserSettings.objects.get(key = "datatable_activity_fields")
        except:
            usersettings = UserSettings()
        usersettings.key = "datatable_activity_fields"
        usersettings.user = user
        usersettings.value = json.dumps(visible_fields)
        usersettings.save()
        return ("visible fields saved")
    
    if (req.get('action') == 'reset'):
        try:
            usersettings = UserSettings.objects.get(key = "datatable_activity_fields")
            usersettings.delete()
        except:
            pass
        return ("visible fields reset")



def show_today_activity(request):
    """Call show_date_activity with current day parameters
    
    :param request: HTTP request parameter
    :type request: HttpRequest
    """
    currentday=datetime.now()
    return (show_date_activity(request,currentday.strftime("%Y-%m-%d"),"latest"))

@login_required
def show_date_activity(request,date,act="latest"):
    """Show activity by date
    
    :param request: HTTP request parameter
    :type request: HttpRequest
    :param date : date parameter in Y-m-d format
    :type request: String
    :param request : Activity id or "latest"
    :type request: String

    :returns: HttpResponse
    :rtype: HttpPage
    """
    if request.method == 'POST':
        msg = __visible_field_save_or_reset(request.POST,request.user)
        return HttpResponse(msg)

    else:
        fields_data = __provide_fields_data(Activity(),"datatable_activity_fields")
        activities = Activity.objects.filter(user_id__username = request.user)
        dateobject = parse(date) # Datetime object comming from url
        activities_in_table = Activity.get_day(dateobject,request.user)
        #print dateobject 
        return render(request, 'ot_logbook/show_date_activity.html', {'activities': activities, 'now':dateobject, 'fields': fields_data["fields"], 'visible_fields': fields_data["visible_fields"], 'activities_in_table' : activities_in_table  })
