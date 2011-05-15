from django.conf import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('msc_qas.views',
    # Example:
    # (r'^msc_qas/', include('msc_qas.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    
    url(r'^$',
        view="index",
        name="index",
    ),
    
    url(r'^logout/$',
        view="logout",
        name="logout",
    ),
    
    url(r'^dashboard/$',
        view="dashboard",
        name="dashboard",
    ),
    
    url(r'course/', include('msc_qas.course.urls')),
)

# serve static files if running DEBUG mode
if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$',
            view   = 'django.views.static.serve',
            kwargs = {
                'document_root':settings.MEDIA_ROOT,
                'show_indexes':True,
            },
        ),
    ) + urlpatterns
