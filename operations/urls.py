from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),
    url(r'^ui/$', 'ui.views.login'),
    url(r'^result/$', 'ui.views.processProcessingForm'),
	url(r'^bookresult/$', 'ui.views.processBookForm'),
    url(r'^logout/$', 'ui.views.logoutUser'),
    url(r'^user/$', 'ui.views.produceData'),
	url(r'^index/$', 'ui.views.indexPage'),
	url(r'^showusers/$', 'ui.views.showUsers'),
	url(r'^inputsession/$', 'ui.views.adminSessionData'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
