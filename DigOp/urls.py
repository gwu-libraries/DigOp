from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, url
from django.views.generic import TemplateView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),
    url(r'^$', 'ui.views.login', name="login"),
    url(r'^processProcessingForm/$', 'ui.views.processProcessingForm', name="processProcessingForm"),
    url(r'^itemProcessingForm/$', 'ui.views.itemProcessingForm', name="itemProcessingForm"),
    url(r'^processBookForm/$', 'ui.views.processBookForm', name="processBookForm"),
    url(r'^showGraph/$', 'ui.views.showGraph', name="showGraph"),
    url(r'^logoutUser/$', 'ui.views.logoutUser', name="logoutUser"),
    url(r'^produceData/$', 'ui.views.produceData', name="produceData"),
    url(r'^indexPage/$', 'ui.views.indexPage', name="indexPage"),
    url(r'^showUsers/$', 'ui.views.showUsers', name="showUsers"),
    url(r'^reportMenu/$', 'ui.views.reportMenu', name="reportMenu"),
    url(r'^barcodePage/$', 'ui.views.barcodePage', name="barcodePage"),
    url(r'^barcodeReport/$', 'ui.views.barcodeReport', name="barcodeReport"),
    url(r'^adminSessionData/$', 'ui.views.adminSessionData', name="adminSessionData"),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^api/', TemplateView.as_view(template_name='api.html'), name="api"),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
