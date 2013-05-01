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

    url(r'^add_project/$', 'ui.views.add_project', name="add_project"),
    url(r'^admin_session_data/$', 'ui.views.admin_session_data', name="admin_session_data"),

    url(r'^barcode/(?P<identifier>\w+)$', 'ui.views.barcode', name='barcode'),
    url(r'^barcode/(?P<identifier>\w+).json$', 'ui.views.barcode_json', name='barcode_json'),
    url(r'^barcode_page/$', 'ui.views.barcode_page', name="barcode_page"),
    url(r'^barcode_report/$', 'ui.views.barcode_report', name="barcode_report"),

    url(r'^close_project/$', 'ui.views.close_project', name="close_project"),

    url(r'^display_item_processing_form/$', 'ui.views.display_item_processing_form', name="display_item_processing_form"),
    url(r'^display_time_line_graph/(?P<identifier>\w+)$', 'ui.views.display_time_line_graph', name="display_time_line_graph"),

    url(r'^index_page/$', 'ui.views.index_page', name="index_page"),
    url(r'^item/(?P<itemtype>\Map|Book|Microfilm).json$', 'ui.views.item_json', name='item_json'),
    url(r'^item/(?P<itemtype>\S{0,9})$', 'ui.views.item', name='item'),
    url(r'^item_processing_form/$', 'ui.views.item_processing_form', name="item_processing_form"),
    url(r'^item_menu/$', 'ui.views.item_menu', name="item_menu"),

    url(r'^login/$', 'ui.views.login', name="login"),
    url(r'^logout_user/$', 'ui.views.logout_user', name="logout_user"),

    url(r'^profiles/edit/$', 'profiles.views.edit_profile', {'form_class': ProfileForm,'success_url': '../../indexPage',},name='edit'),
    url(r'^profiles/', include('profiles.urls')),
    url(r'^profile_menu/$','ui.views.profile_menu', name='profile_menu'),

    url(r'^password_change/$','django.contrib.auth.views.password_change', {'template_name': 'accounts/password_change_form.html'},name='password_change'),
    url(r'^password_change_done/$','django.contrib.auth.views.password_change_done', {'template_name': 'accounts/my_password_change_done.html'}),
    url(r'^password_reset_complete$', 'django.contrib.auth.views.password_reset_complete', {'template_name': 'password_reset_complete.html'}),
    url(r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done', {'template_name': 'reset_done.html'}),

    url(r'^process_book_form/$', 'ui.views.process_book_form', name="process_book_form"),
    url(r'^process_item_form/$', 'ui.views.process_item_form', name="process_item_form"),
    url(r'^process_processing_form/$', 'ui.views.process_processing_form', name="process_processing_form"),

    url(r'^produce_data/$', 'ui.views.produce_data', name="produce_data"),

    url(r'^project_data/(?P<identifier>\w+)$', 'ui.views.project_data', name='project_data'),
    url(r'^project_data/(?P<identifier>\w+).json$', 'ui.views.project_data_json', name='project_data_json'),
    url(r'^project_form/$', 'ui.views.project_form', name="project_form"),
    
    url(r'^report_menu/$', 'ui.views.report_menu', name="report_menu"),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name': 'password_reset_confirm.html'}),
    url(r'^reset_password/$', 'django.contrib.auth.views.password_reset', {'template_name': 'reset_password.html'}, name='reset_password'),
    
    url(r'^show_graph/(?P<chartType>[a-z]+)/(?P<project>\w+)/$', 'ui.views.show_graph', name="show_graph"),
    url(r'^show_projects/$', 'ui.views.show_projects', name="show_projects"),
    url(r'^show_users/$', 'ui.views.show_users', name="show_users"),
    
    url(r'^task/(?P<tasktype>\S{2,4})$', 'ui.views.task', name='task'),
    url(r'^task/(?P<tasktype>\S{2,4}).json$', 'ui.views.task_json', name='task_json'),
    
    url(r'^user/(?P<username>[\w.@+-]+)/$', 'ui.views.user', name='user'),
    url(r'^user/(?P<username>[\w.@+-]+).json$', 'ui.views.user_json', name='user_json'),

    url(r'^view_profile/$','ui.views.view_profile', name='view_profile'),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^accounts/', include('registration.backends.default.urls')),
)
