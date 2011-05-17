from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.views import logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.conf import settings

from course.models import Course
MAX_COMPLETED_SHOWN = 5

def index(request, template_name="index.html"):
    "If logged in, redirect to dashboard. Else, show login form"
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard'))
    
    return auth_login(request, template_name, redirect_field_name='next')
    
def logout(request):
    "Custom logout view with next_page = settings.LOGIN_URL"
    return auth_logout(request, next_page=settings.LOGIN_URL)
    
@login_required
def dashboard(request, template_name="dashboard.html"):
    roles = [g.name for g in request.user.groups.all()]
    c = {"roles":roles}
    
    if "manager" in roles:  # managers (observer) can see all active courses
        # TODO: pending approvals
        active = Course.objects.filter(activated=True)
        c["mgr_current_courses"] = active.filter(complete=False)
        c["mgr_completed_courses"] = active.filter(complete=True)[:MAX_COMPLETED_SHOWN]
    
    if "course_admin" in roles:
        current = request.user.course_administered.filter(complete=False)
        archive = request.user.course_administered.filter(complete=True)
        c["adm_inactive_courses"] = current.filter(activated=False)
        c["adm_current_courses"] = current.filter(activated=True)
        c["adm_completed_courses"] = archive[:MAX_COMPLETED_SHOWN]

    # all users are devs. Only see courses they've been assigned to
    course_dev = request.user.course_developed.filter(activated=True)
    c["current_courses"] =  course_dev.filter(complete=False)
    c["completed_courses"] = course_dev.filter(complete=True)[:MAX_COMPLETED_SHOWN]
    
    #courses_active = request.user.course_administered.filter(activated=True) #, complete=False
    return render_to_response(template_name, c, context_instance=RequestContext(request))
    
    

