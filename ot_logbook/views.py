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

def last_week_activity(request):
    """Get activities from last 7 days
    
    :param request: HTTP request parameter
    :type request: HttpRequest

    :returns: HttpResponse
    :rtype: HttpPage
    """
    lastweek = Activity.objects.filter(public = True).filter(datetime__gt = datetime.now()-timedelta(days=7))
    return render(request, 'ot_logbook/lastweek_activity.html', {'lastweek': lastweek})

def public_activities(request):
    """Get public activities.
    
    :param request: HTTP request
    :type request: HttpRequest

    :returns: HttpResponse
    :rtype: HttpPage
    """
    if request.method == 'POST':
        toto = request.POST
        print json.dumps(toto.getlist('visible_fields'))
        #print toto.getlist('visible_fields')
        return HttpResponse("OK")
    else:
        activities = Activity.objects.filter(public = True)
        act = Activity() # Create a activity object to get all fields
        fields = act.get_all_fields()
        # Get user or global settings regarding fields visible
        try:
            visible_fields = UserSettings.objects.get(key = "datatable_activity_fields")
        except:
            visible_fields = GlobalSettings.objects.get(key = "datatable_activity_fields")

        vf = visible_fields.value
        visible_fields = json.loads(vf)

        return render(request, 'ot_logbook/public_activities.html', {'fields': fields, 'activities': activities, 'visible_fields': visible_fields })

@login_required
def show_today_activity(request):
    """Show today activity
    
    :param request: HTTP request parameter
    :type request: HttpRequest

    :returns: HttpResponse
    :rtype: HttpPage
    """
    #last3months = Activity.objects.filter(public = False).filter(user_id__username = request.user)
    activities = Activity.objects.filter(user_id__username = request.user)
    return render(request, 'ot_logbook/show_today_activity.html', {'activities': activities})
