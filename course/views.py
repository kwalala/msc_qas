from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings

from course.forms import CourseForm

def course_add(request, template_name="course/add.html"):
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.admin = request.user
            course.save()
            return HttpResponseRedirect(reverse('course_activate', 
                        kwargs={"id":course.id}))
    else:
        form = CourseForm()
    
    return render_to_response(template_name, {
        'form' : form,
    }, context_instance=RequestContext(request))
