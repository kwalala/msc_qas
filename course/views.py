from datetime import date

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib import messages

from course.forms import CourseForm
from course.defaults import MILESTONE_TEMPLATES
from course.models import Milestone, Task, Course

@login_required
def course_add(request, template_name="course/add.html"):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.admin = request.user
            course.save()
            course.developers.add(course.leader)
            return HttpResponseRedirect(reverse('course_activate', 
                        kwargs={"cid":course.id}))
    else:
        form = CourseForm()
    
    return render_to_response(template_name, {
        'form' : form,
    }, context_instance=RequestContext(request))

@login_required
def course_activate(request, cid, template_name="course/activate.html"):
    course = get_object_or_404(request.user.course_administered,
                    id=cid, activated=False)
    if request.method == "POST":
        appr = User.objects.get(username__exact=settings.DEFAULT_APPROVER)
        print request.POST
        for ms_name in request.POST.getlist("milestone"):
            # TODO: error checks ,,,
            m = Milestone(name=ms_name, course=course, approver=appr,
                    date_target=course.date_target)
            m.save()
        course.activated = True
        course.save()
        
        messages.success(request, 
            "%s has been activated. Leader (%s) will be informed" \
                % (course.name, course.leader.get_full_name()))
            
        return HttpResponseRedirect(reverse('dashboard'))
            
        
    milestones = MILESTONE_TEMPLATES[course.category]
    return render_to_response(template_name, {
        'course': course,
        'milestones': milestones
    }, context_instance=RequestContext(request))
    
@login_required
def course_view(request, cid, template_name="course/view.html"):
    course = get_object_or_404(Course, id=cid, activated=True)
    if request.user != course.admin \
            and not course.developers.filter(id=request.user.id).exists() \
            and not request.user.groups.filter(name="manager").exists():
        return HttpResponseForbidden("Access Forbidden")
        
    if course.date_target <= date.today():
        course_due = True
    else:
        course_due = False
        
    return render_to_response(template_name, {
        'course': course,
        'course_due': course_due,
        'milestones': course.milestone_set.all(),
    }, context_instance=RequestContext(request))       
        
@login_required
def milestone_edit(request, cid, mid, template_name="course/milestone.html"):
    course = get_object_or_404(Course, id=cid, activated=True, complete=False)
    if request.user not in (course.leader, course.admin):
        return HttpResponseForbidden("Access Forbidden")
    milestone = get_object_or_404(course.milestone_set, id=mid)
    return render_to_response(template_name, {
        'course': course,
        'milestone': milestone,
        'tasks' : milestone.task_set.all(),
        'developers': Group.objects.get(name="developer").user_set.all(),
    }, context_instance=RequestContext(request)) 
        
#@login_required
#def course_view(request, cid, template_name="course/view.html"):
    #course = get_object_or_404(request.user.course_developed,
                    #id=cid, activated=True)
                    
    #if request.is_ajax():
        ## TODO: error checks
        #task_name = request.POST["task_name"]
        #user_id = request.POST["user_id"]
        #ms_id = request.POST["ms_id"]
        
        #milestone = course.milestone_set.get(id=ms_id)
        #dev = course.developers.get(id=user_id)
        #task = Task(name=task_name, milestone=milestone, developer=dev)
        #task.save()
        #return HttpResponse("OK")
        
    #return render_to_response(template_name, {
        #'course' : course,
    #}, context_instance=RequestContext(request))
    
    