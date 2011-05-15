from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings

from course.forms import CourseForm
from course.defaults import MILESTONE_TEMPLATES

def course_add(request, template_name="course/add.html"):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.admin = request.user
            course.save()
            return HttpResponseRedirect(reverse('course_activate', 
                        kwargs={"cid":course.id}))
    else:
        form = CourseForm()
    
    return render_to_response(template_name, {
        'form' : form,
    }, context_instance=RequestContext(request))

def course_activate(request, cid, template_name="course/activate.html"):
    course = get_object_or_404(request.user.course_administered,
                    id=cid, activated=False)
    milestones = MILESTONE_TEMPLATES[course.category]
    return render_to_response(template_name, {
        'course': course,
        'milestones': milestones
    }, context_instance=RequestContext(request))