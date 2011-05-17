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
    incomplete_courses = request.user.course_administered.filter(activated=False)
    courses = request.user.course_administered.filter(activated=True) #, complete=False
    course_dev = request.user.course_developed.filter(activated=True)
    courses_dev_active =  course_dev.filter(complete=False)
    courses_dev_completed = course_dev.filter(complete=True)
    
    #courses_active = request.user.course_administered.filter(activated=True) #, complete=False
    return render_to_response(template_name, {
        "incomplete_courses": incomplete_courses,
        "courses": courses,
        "courses_dev_active": courses_dev_active,
        "courses_dev_completed": courses_dev_completed,
    }, context_instance=RequestContext(request))
    
    

