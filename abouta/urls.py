from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'abouta.views.main'),
    url(r'^join/$', 'abouta.views.join'),
    url(r'^committees/$', 'abouta.views.committees'),
    url(r'^committees/(?P<id>\d+)$', 'abouta.views.committees_details'),
    url(r'^corporate/$', 'abouta.views.corporate'),
    url(r'^corporate/job/$', 'abouta.views.job'),
    url(r'^corporate/job/thanks/$', 'abouta.views.thanks'),
    url(r'^members/$', 'abouta.views.members'),
)


 