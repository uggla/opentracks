# Create your views here.

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from models import Activity
from datetime import datetime, date, time, tzinfo, timedelta

def last_week_activity(request):
    """Get activities from last 7 days
    
    :param request: HTTP request parameter
    :type request: HttpRequest

    :returns: HttpResponse
    :rtype: HttpPage
    """
    lastweek = Activity.objects.filter(public = True).filter(datetime__gt = datetime.now()-timedelta(days=7))
    return render(request, 'ot_logbook/lastweek_activity.html', {'lastweek': lastweek})

def show_today_activity(request):
    """Show today activity
    
    :param request: HTTP request parameter
    :type request: HttpRequest

    :returns: HttpResponse
    :rtype: HttpPage
    """
    last3months = Activity.objects.filter(public = True)
    return render(request, 'ot_logbook/show_today_activity.html', {'last3months': last3months})
