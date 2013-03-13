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
    url(r'^profile_menu/$','ui.views.profile_menu', name='profile_menu'),
    url(r'^password_change/$','django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html'},name='password_change'),
    url(r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'reset_done.html'}),
    url(r'^password_change_done/$','django.contrib.auth.views.password_change_done', {'template_name': 'accounts/my_password_change_done.html'}),
    #url(r'^password_change_done/$','ui.views.password_change_done', name='password_change_done'),
    #url(r'^password_reset_done/$','ui.views.reset_done', name='reset_done'),
    url(r'^view_profile/$','ui.views.view_profile', name='view_profile'),
    url(r'^reset_password/$', 'django.contrib.auth.views.password_reset', {'template_name': 'reset_password.html'}, name='reset_password'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html'}),
    url(r'^password_reset_complete$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_complete.html'}),
    url(r'^login/$', 'ui.views.login', name="login"),
    url(r'^user/(?P<username>[\w.@+-]+)/$', 'ui.views.user', name='user'),
    url(r'^user/(?P<username>[\w.@+-]+).json$', 'ui.views.user_json', name='user_json'),
    url(r'^task/(?P<tasktype>\S{2,4})$', 'ui.views.task', name='task'),
    url(r'^task/(?P<tasktype>\S{2,4}).json$', 'ui.views.task_json', name='task_json'),
    url(r'^item/(?P<itemtype>\Map|Book|Microfilm).json$', 'ui.views.item_json', name='item_json'),
    url(r'^item/(?P<itemtype>\S{0,9})$', 'ui.views.item', name='item'),
    url(r'^barcode/(?P<identifier>\w+)$', 'ui.views.barcode', name='barcode'),
    url(r'^barcode/(?P<identifier>\w+).json$', 'ui.views.barcode_json', name='barcode_json'),
    url(r'^projectData/(?P<identifier>\w+)$', 'ui.views.projectData', name='projectData'),
    url(r'^projectData/(?P<identifier>\w+).json$', 'ui.views.projectData_json', name='projectData_json'),
    url(r'^processProcessingForm/$', 'ui.views.processProcessingForm', name="processProcessingForm"),
    url(r'^itemProcessingForm/$', 'ui.views.itemProcessingForm', name="itemProcessingForm"),
    url(r'^itemMenu/$', 'ui.views.itemMenu', name="itemMenu"),
    url(r'^project/$', 'ui.views.project', name="project"),
    url(r'^projectForm/$', 'ui.views.projectForm', name="projectForm"),
    url(r'^closeProject/$', 'ui.views.closeProject', name="closeProject"),
    url(r'^processBookForm/$', 'ui.views.processBookForm', name="processBookForm"),
    url(r'^addProject/$', 'ui.views.addProject', name="addProject"),
    url(r'^showGraph/(?P<chartType>[a-z]+)/$', 'ui.views.showGraph', name="showGraph"),
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
    #url(r'^accounts/', include('registration.backends.default.urls')),
)
