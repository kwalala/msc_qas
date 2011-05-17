from django.conf import settings
from django.conf.urls.defaults import *


urlpatterns = patterns('msc_qas.course.views',
    url('^new/$',
        view="course_add",
        name="course_add",
    ),
    
    url('^(?P<cid>\d+)/activate/$',
        view="course_activate",
        name="course_activate",
    ),
    
    url('^(?P<cid>\d+)/$',
        view="course_view",
        name="course_view",
    ),
    
    url('^(?P<cid>\d+)/milestone/(?P<mid>\d+)$',
        view="milestone_edit",
        name="milestone_edit",
    ),
    
    url('^a/(?P<cid>\d+)/m/(?P<mid>\d+)/t/add$',
        view="ajax_add_tasks",
        name="ajax_add_tasks",
    ),
    
    url('^a/(?P<cid>\d+)/m/(?P<mid>\d+)/t/(?P<tid>\d+)/done',
        view="ajax_mark_task_done",
        name="ajax_mark_task_done",
    ),
    
    
)

