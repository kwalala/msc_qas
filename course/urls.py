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
)

