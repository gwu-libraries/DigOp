from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from ui.models import ProfileForm

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^project/', include('project.foo.urls')),
    url(r'^$', 'ui.views.login', name="login"),
    url(r'^profiles/edit/$', 'profiles.views.edit_profile', {'form_class': ProfileForm,'success_url': '../../indexPage',},name='edit'),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^login/$', 'ui.views.login', name="login"),
    url(r'^user/(?P<username>[\w.@+-]+)/$', 'ui.views.user', name='user'),
    url(r'^task/(?P<tasktype>\S{2,4})$', 'ui.views.task', name='task'),
    url(r'^item/(?P<itemtype>\S{0,9})$', 'ui.views.item', name='item'),
    url(r'^barcode/(?P<identifier>\S{2,25})$', 'ui.views.barcode', name='barcode'),
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
    url(r'^displayItemProcessingForm/$', 'ui.views.displayItemProcessingForm', name="displayItemProcessingForm"),
    url(r'^processItemForm/$', 'ui.views.processItemForm', name="processItemForm"),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name="about"),
    url(r'^api/', TemplateView.as_view(template_name='api.html'), name="api"),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
