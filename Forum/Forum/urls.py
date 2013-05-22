from django.conf.urls import patterns, include, url
from Thread.views import login, register, edit_profile

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Forum.views.home', name='home'),
    # url(r'^Forum/', include('Forum.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
 	url(r'^register/$', register),
 	url(r'^edit-profile/{0,1}$', edit_profile),
 	url(r'^()$', login),
 	url(r'^accounts/log((?:in)|(?:out))/$', login),
)
